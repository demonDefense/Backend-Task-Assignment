import os
import sys
import datetime
from passlib.context import CryptContext

# Ensure project root is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from database import SessionLocal, engine
from app.models.models import Base, User, Role, UserRole

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def populate_admin_user():
    db = SessionLocal()
    try:
        admin_role = db.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="ecommerce admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        admin_user = db.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@shop.com",
                password_hash=hash_password("admin123"),
                created_at=datetime.datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

        existing = db.query(UserRole).filter_by(user_id=admin_user.id, role_id=admin_role.id).first()
        if not existing:
            mapping = UserRole(
                user_id=admin_user.id,
                role_id=admin_role.id,
                assigned_at=datetime.datetime.utcnow()
            )
            db.add(mapping)
            db.commit()

        print("Admin user and role created successfully.")
    finally:
        db.close()

if __name__ == '__main__':
    populate_admin_user()
