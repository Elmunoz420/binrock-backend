import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv  # Import load_dotenv

# --- Config de Postgres en Render ---
load_dotenv()  # carga variables de .env
DATABASE_URL = os.getenv("DATABASE_URL")

# pool_pre_ping=True asegura que no se usen conexiones muertas
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=280,   # recicla conexiones cada ~5 minutos
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia que inyecta la sesión en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
