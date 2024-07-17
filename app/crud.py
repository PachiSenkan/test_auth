from sqlalchemy.orm import Session

from app import schemas
from app.models import User
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user_create: schemas.UserCreate):
    db_user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        is_superuser=False,
        hashed_password=get_password_hash(user_create.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, limit: int = 100, skip: int = 0) -> list[User | None]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def update_user(db: Session, new_user: schemas.UserUpdateMe, old_user: User):
    new_user_dict = new_user.model_dump(exclude_unset=True, exclude_none=True)
    print(new_user_dict)
    if "password" in new_user_dict:
        password = new_user_dict["password"]
        hashed_password = get_password_hash(password)
        new_user_dict["hashed_password"] = hashed_password
        del new_user_dict["password"]
    print(new_user_dict)
    db.query(User).filter(User.id == old_user.id).update(
        new_user_dict, synchronize_session=False
    )
    db.commit()


def update_user_by_id(db: Session, new_user: schemas.UserUpdate, old_user_id: int):
    new_user_dict = new_user.model_dump(exclude_unset=True, exclude_none=True)
    db.query(User).filter(User.id == old_user_id).update(
        new_user_dict, synchronize_session=False
    )
    db.commit()


def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(db=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
