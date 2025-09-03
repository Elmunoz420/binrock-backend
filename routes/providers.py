# routes/providers.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.provider import Provider  # 👈 asegúrate que exista el modelo
from schemas.provider import ProviderResponse  # 👈 crea el schema

router = APIRouter()

# Listar todos los proveedores
@router.get("/providers", response_model=list[ProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()
