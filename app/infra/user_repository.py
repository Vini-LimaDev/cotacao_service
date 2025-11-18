# app/infra/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.user_models import User
from app.domain.auth_schemas import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    """Repositório para operações com usuários no banco de dados"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create(self, user_data: UserCreate) -> User:
        """Cria um novo usuário"""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def email_exists(self, email: str) -> bool:
        """Verifica se email já está cadastrado"""
        return self.get_by_email(email) is not None
    
    def list_all(self, skip: int = 0, limit: int = 100):
        """Lista todos os usuários"""
        return self.db.query(User).offset(skip).limit(limit).all()
