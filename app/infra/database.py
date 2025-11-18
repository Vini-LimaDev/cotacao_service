# app/infra/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cria o engine do SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica a conexão antes de usar
    echo=False,  # Mude para True para debug SQL
)

# Cria a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class para os modelos
Base = declarative_base()


def get_db():
    """
    Dependency que fornece uma sessão do banco de dados.
    Usa-se como: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
