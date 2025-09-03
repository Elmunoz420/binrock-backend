from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from db import get_db
from models.order import Order, OrderItem, OrderEvent
from models.customer import Customer
from models.order_status import OrderStatus
from models.user import Role
from routes.auth import get_current_user   # importa desde donde tengas auth
from schemas.order import OrderCreate, OrderResponse

router = APIRouter()


# --- Helper para enmascarar datos según rol ---
def mask_order(order: Order, role: Role):
    base = {
        "id": order.id,
        "customer_id": order.customer_id,
        "address_id": order.address_id,
        "country_code": order.country_code,
        "currency_code": order.currency_code,
        "status_code": order.status_code,
        "items_count": order.items_count,
        "subtotal": order.subtotal,
        "shipping_fee": order.shipping_fee,
        "shipping_paid_by_customer": order.shipping_paid_by_customer,
        "total_paid": order.total_paid,
        "notes": order.notes,
        "created_at": order.created_at,
        "provider_id": order.provider_id,
        "events": [
            {
                "id": ev.id,
                "order_id": ev.order_id,
                "event_type": ev.event_type,
                "from_status": ev.from_status,
                "to_status": ev.to_status,
                "note": ev.note,
                "created_at": ev.created_at,
            }
            for ev in order.events
        ],
        "items": [
            {
                "id": it.id,
                "product_id": it.product_id,
                "quantity": it.quantity,
                "unit_price": it.unit_price if role in (Role.ADMIN, Role.OPERACIONES) else None,
                "unit_cost": it.unit_cost,
                "size": it.size,
                "product": {
                    "id": it.product.id if it.product else None,
                    "sku_base": it.product.sku_base if it.product else None,
                    "name": it.product.name if it.product else None,
                } if it.product else None,
            }
            for it in order.items
        ],
        "customer": {
            "id": order.customer.id if order.customer else None,
            "full_name": order.customer.full_name if order.customer else None,
            "email": order.customer.email if role in (Role.ADMIN, Role.OPERACIONES) else None,
            "phone": order.customer.phone if order.customer else None,
            "ig_username": order.customer.ig_username if order.customer else None,
            "national_id": order.customer.national_id if order.customer else None,
        } if order.customer else None,
        "address": {
            "id": order.address.id if order.address else None,
            "street1": order.address.street1 if order.address else None,
            "street2": order.address.street2 if order.address else None,
            "city": order.address.city if order.address else None,
            "state": order.address.state if order.address else None,
            "postal_code": order.address.postal_code if order.address else None,
            "country_code": order.address.country_code if order.address else None,
            "label": order.address.label if order.address else None,
        } if order.address else None,
    }
    return base



# --- Endpoints ---

@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.address),
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.events)
        )
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role == Role.PROVEEDOR and order.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    return mask_order(order, current_user.role)


@router.get("/orders")
def list_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    customer_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None)
):
    q = db.query(Order).options(
        joinedload(Order.customer),
        joinedload(Order.address),
        joinedload(Order.items).joinedload(OrderItem.product),
        joinedload(Order.events)
    )

    if customer_id:
        q = q.filter(Order.customer_id == customer_id)
    if status:
        q = q.filter(Order.status_code == status)
    if date_from:
        q = q.filter(Order.created_at >= date_from)
    if date_to:
        q = q.filter(Order.created_at <= date_to)

    if current_user.role == Role.PROVEEDOR:
        q = q.filter(Order.provider_id == current_user.id)

    # 👇 aquí impones FIFO
    q = q.order_by(Order.created_at.asc())

    orders = q.all()
    return [mask_order(o, current_user.role) for o in orders]



@router.post("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Solo el Admin puede cancelar
    if new_status == "cancelado" and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Solo Admin puede cancelar pedidos")

    # Proveedor puede avanzar estados
    if current_user.role == Role.PROVEEDOR:
        if new_status not in ["en_proceso", "entregado"]:
            raise HTTPException(status_code=403, detail="Estado no permitido para proveedor")

    valid_status = db.query(OrderStatus).filter(OrderStatus.code == new_status).first()
    if not valid_status:
        raise HTTPException(status_code=400, detail="Estado inválido")

    prev_status = order.status_code
    order.status_code = new_status

    event = OrderEvent(
        order_id=order.id,
        event_type="status_change",
        from_status=prev_status,
        to_status=new_status,
        note="Cambio de estado",
        created_at=datetime.now()
    )
    db.add(event)

    db.commit()
    db.refresh(order)
    return mask_order(order, current_user.role)

@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not order_data.items or len(order_data.items) == 0:
        raise HTTPException(status_code=400, detail="El pedido debe tener al menos un producto")

    subtotal = sum(i.quantity * i.unit_price for i in order_data.items)
    total_paid = subtotal + (order_data.shipping_fee if order_data.shipping_paid_by_customer else 0)

    order = Order(
        customer_id=order_data.customer_id,
        address_id=order_data.address_id,
        country_code=order_data.country_code,
        currency_code=order_data.currency_code,
        status_code="recibido",
        items_count=sum(i.quantity for i in order_data.items),
        subtotal=subtotal,
        shipping_fee=order_data.shipping_fee,
        shipping_paid_by_customer=order_data.shipping_paid_by_customer,
        total_paid=total_paid,
        notes=order_data.notes,
        created_at=datetime.utcnow(),
        provider_id=order_data.provider_id
    )
    db.add(order)
    db.flush()  # para obtener el ID

    for it in order_data.items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=it.product_id,
            quantity=it.quantity,
            unit_price=it.unit_price,
            unit_cost=it.unit_cost,
            size=it.size
        ))

    db.commit()
    db.refresh(order)
    return mask_order(order, current_user.role)
