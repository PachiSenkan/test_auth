from sqlalchemy import Boolean, Column, Integer, String

from .core.db import Base


class User(Base):
    """
    Информация о пользователях
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_superuser = Column(Boolean)
