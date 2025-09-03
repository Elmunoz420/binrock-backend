from fastapi import FastAPI
from routes import products, customers, orders, auth
from db import engine, Base

# 👇 Importa todos los modelos explícitamente
from models.customer import Customer
from models.address import Address
from models.country import Country
from models.product import Product
from models.order import Order, OrderItem, OrderEvent
from models.order_status import OrderStatus
from models.currency import Currency
from models.provider import Provider
from models.user import User, Role


app = FastAPI(title="Binrock API")

# Crea las tablas si no existen
#Base.metadata.create_all(bind=engine)

app.include_router(products.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API funcionando 🚀 con FastAPI y SQLAlchemy"}
