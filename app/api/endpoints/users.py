from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from app.crud.user_crud import *
from app.schemas.schemas import UserCreate, RoleCreate, User as UserSchema, Role as RoleSchema, UserRoleBase, LoginRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        roles = payload.get("roles", [])
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login First", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login First", headers={"WWW-Authenticate": "Bearer"})

    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login First", headers={"WWW-Authenticate": "Bearer"})

    user.token_roles = roles
    return user

def Isadmin(token: str, db: Session):
    current_user=get_current_user(token, db)
    if "admin" not in current_user.token_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return True
    
@router.post("/login", tags=["Auth"])
def login_for_access_token(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    user.last_login = datetime.utcnow()
    db.commit()
    user_roles = [role.name for role in user.roles]
    access_token = create_access_token(data={"sub": user.username}, roles=user_roles)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/Create_User/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if Isadmin(user_in.token, db):
        return create_user(db, user_in)

@router.get("/Get_All_Users/", response_model=List[UserSchema], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_users(db, skip=skip, limit=limit)

@router.get("/Get_User/{user_id}", response_model=UserSchema, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/Update_User/{user_id}", response_model=UserSchema, tags=["Users"])
def update_existing_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    if Isadmin(user_in.token, db):
        updated = update_user(db, user_id, user_in)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated

@router.delete("/Delete_User/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None

@router.post("/Create_Role/", response_model=RoleSchema, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def create_new_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role_in)

@router.get("/Get_All_Roles/", response_model=List[RoleSchema], tags=["Roles"])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_roles(db, skip, limit)

@router.get("/Get_Role/{role_id}", response_model=RoleSchema, tags=["Roles"])
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role

@router.put("/Update_Role/{role_id}", response_model=RoleSchema, tags=["Roles"])
def update_existing_role(role_id: int, role_in: RoleCreate, db: Session = Depends(get_db)):
    updated = update_role(db, role_id, role_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return updated

@router.delete("/Delete_Role/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
    success = delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return None    
    
@router.post("/Assign_Role/{user_id}/role/{role_id}", response_model=UserRoleBase, tags=["User_Role"])
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    user_role = assign_role_to_user(db, user_id, role_id)
    return user_role

@router.get("/users/{user_id}/roles/{role_id}", response_model=UserRoleBase, tags=["User_Role"])
def get_user_role_mapping(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user_role = get_user_role(db, user_id, role_id)
    if not user_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRole not found")
    return user_role
    
@router.get("/users/{user_id}/roles", response_model=List[UserRoleBase], tags=["User_Role"])
def get_user_roles_mapping(user_id: int, db: Session = Depends(get_db)):
    user_roles = get_user_roles(db, user_id)
    if not user_roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRole not found")
    return user_roles

@router.put("/users/{user_id}/roles/{role_id}", response_model=UserRoleBase, tags=["User_Role"])
def update_user_role_mapping(user_id: int, role_id: int, new_role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, new_role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    updated = update_user_role(db, user_id, role_id, new_role_id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRole not found")
    return updated

@router.delete("/users/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User_Role"])
def delete_user_role_mapping(user_id: int, role_id: int, db: Session = Depends(get_db)):
    success = delete_user_role(db, user_id, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRole not found")
    return None
