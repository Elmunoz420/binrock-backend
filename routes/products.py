from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.product import Product
from models.product_price import ProductPrice   # 👈 importar
from models.product_cost import ProductCost     # 👈 importar
from schemas.product import ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def list_products(q: str = "", db: Session = Depends(get_db)):
    query = db.query(Product)
    if q:
        q_lower = f"%{q.lower()}%"
        query = query.filter(
            (Product.sku_base.ilike(q_lower)) |
            (Product.name.ilike(q_lower))
        )
    products = query.all()
    result = []
    for p in products:
        price = db.query(ProductPrice).filter(ProductPrice.product_id==p.id).order_by(ProductPrice.effective_from.desc()).first()
        cost = db.query(ProductCost).filter(ProductCost.product_id==p.id).order_by(ProductCost.effective_from.desc()).first()
        result.append({
            "id": p.id,
            "sku_base": p.sku_base,
            "name": p.name,
            "description": p.description,
            "is_active": p.is_active,
            "created_at": p.created_at,
            "price": float(price.price) if price else 0,
            "cost": float(cost.cost) if cost else 0
        })
    return result