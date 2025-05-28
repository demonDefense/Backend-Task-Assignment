from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from passlib.context import CryptContext
from fastapi import Depends
import jwt
import os
from dotenv import load_dotenv

from app.models.models import User, Role, UserRole
from app.schemas.schemas import UserCreate, RoleCreate

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, roles: List[str], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    to_encode.update({"roles": roles})
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password_hash):
        return user
    return None

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password)  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_in: UserCreate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.username = user_in.username
    db_user.email = user_in.email
    db_user.password_hash = hash_password(user_in.password)
    db_user.last_login = db_user.last_login
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()


def list_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    return db.query(Role).offset(skip).limit(limit).all()


def create_role(db: Session, role_in: RoleCreate) -> Role:
    db_role = Role(**role_in.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_in: RoleCreate) -> Optional[Role]:
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    db_role.name = role_in.name
    db_role.description = role_in.description
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int) -> bool:
    db_role = get_role(db, role_id)
    if not db_role:
        return False
    db.delete(db_role)
    db.commit()
    return True

def assign_role_to_user(db: Session, user_id: int, role_id: int) -> UserRole:
    user_role = UserRole(
        user_id=user_id,
        role_id=role_id,
        assigned_at=datetime.utcnow()
    )
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role

def get_user_role(db: Session, user_id: int, role_id: int) -> Optional[UserRole]:
    return db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()

def get_user_roles(db: Session, user_id: int) -> List[UserRole]:
    return db.query(UserRole).filter(
        UserRole.user_id == user_id
    ).all()


def update_user_role(db: Session, user_id: int, old_role_id: int, new_role_id: int) -> Optional[UserRole]:
    user_role = get_user_role(db, user_id, old_role_id)
    if not user_role:
        return None
    user_role.role_id = new_role_id
    user_role.assigned_at = datetime.utcnow()
    db.commit()
    db.refresh(user_role)
    return user_role


def delete_user_role(db: Session, user_id: int, role_id: int) -> bool:
    user_role = get_user_role(db, user_id, role_id)
    if not user_role:
        return False
    db.delete(user_role)
    db.commit()
    return True
