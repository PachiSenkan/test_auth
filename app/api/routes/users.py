from typing import Any
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user, get_db, get_current_active_superuser
from app import crud, schemas

router = APIRouter()


@router.get(
    "/", response_model=list[schemas.User], dependencies=[Depends(get_current_user)]
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список всех пользователей
    """
    users = crud.get_users(limit=limit, skip=skip, db=db)
    return users


@router.get(
    "/{user_id}",
    response_model=schemas.User | None,
    dependencies=[Depends(get_current_user)],
)
def read_user(user_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Получить пользователя по id
    """
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get(
    "/admin/{user_id}",
    response_model=schemas.UserFull | None,
    dependencies=[Depends(get_current_active_superuser)],
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получить пользователя по id (полная информация)
    """
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get(
    "/admin",
    response_model=list[schemas.UserFull],
    dependencies=[Depends(get_current_active_superuser)],
)
def read_users_admin(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список всех пользователей (полная информация)
    """
    users = crud.get_users(limit=limit, skip=skip, db=db)
    return users


@router.get("/me", response_model=schemas.UserMe)
def read_users(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Получить активного пользователя
    """
    return current_user


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate = Depends(), db: Session = Depends(get_db)):
    """
    Создать пользователя
    """
    user = crud.get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким адресом электронной почты уже существует",
        )
    user = crud.create_user(db=db, user_create=user_in)
    return user


@router.delete(
    "/delete/{user_id}", dependencies=[Depends(get_current_active_superuser)]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удалить пользователя
    """
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException("Пользователь не найден")
    crud.delete_user(db=db, user=user)
    return {"Message": "Пользователь удален"}


@router.delete("/me/delete")
def delete_user_me(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Удалить активного пользователя
    """
    crud.delete_user(db=db, user=current_user)
    return {"Message": "Пользователь удален"}


@router.patch("/me")
def update_user_me(
    user_in: schemas.UserUpdateMe = Depends(),
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Обновить данные активного пользователя
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="Данный адрес уже зарегистрирован"
            )
    crud.update_user(db=db, new_user=user_in, old_user=current_user)
    return {"Message": "Успешно"}


@router.patch("/update/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate = Depends(),
    db: Session = Depends(get_db),
):
    """
    Обновить данные пользователя
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="Данный адрес уже зарегистрирован"
            )
    crud.update_user_by_id(db=db, new_user=user_in, old_user_id=user_id)
    return {"Message": "Успешно"}
