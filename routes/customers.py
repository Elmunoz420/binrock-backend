from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db import get_db
from models.customer import Customer
from models.address import Address
from schemas.customer import CustomerCreate, CustomerResponse
from schemas.address import AddressCreate, AddressResponse
from typing import List, Optional

router = APIRouter()

# Crear cliente
@router.post("/customers", response_model=CustomerResponse)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    try:
        customer = Customer(
            full_name=data.full_name,
            email=data.email,
            ig_username=data.ig_username,
            phone=data.phone,
            national_id=data.national_id,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Listar clientes con búsqueda
@router.get("/customers", response_model=List[CustomerResponse])
def list_customers(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Customer)
    if q:
        q_lower = f"%{q.lower()}%"
        query = query.filter(
            (Customer.full_name.ilike(q_lower)) |
            (Customer.email.ilike(q_lower)) |
            (Customer.national_id.ilike(q_lower))
        )
    return query.limit(5).all()

# Detalle cliente
@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer

# Añadir dirección a cliente
@router.post("/customers/{customer_id}/addresses", response_model=AddressResponse)
def add_address(customer_id: int, data: AddressCreate, db: Session = Depends(get_db)):
    try:
        # validar cliente
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        address = Address(
            customer_id=customer_id,
            street1=data.street1,
            street2=data.street2,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country_code=data.country_code,
            label=data.label
        )

        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Listar direcciones de un cliente
@router.get("/customers/{customer_id}/addresses", response_model=List[AddressResponse])
def list_addresses(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return db.query(Address).filter(Address.customer_id == customer_id).all()
