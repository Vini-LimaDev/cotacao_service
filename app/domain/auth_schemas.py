# app/domain/auth_schemas.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Schema base para usuário"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str = Field(..., min_length=6, description="Senha deve ter no mínimo 6 caracteres")


class UserResponse(UserBase):
    """Schema para resposta de usuário (sem senha)"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Permite criar a partir de modelos SQLAlchemy


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para dados extraídos do token"""
    email: Optional[str] = None
