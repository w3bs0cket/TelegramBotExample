from .base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import SmallInteger, Integer, String, DateTime, Boolean, func
from sqlalchemy.sql import false

class Settings(BaseModel):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(SmallInteger, autoincrement=True, primary_key=True)
    up_delay: Mapped[int] = mapped_column(Integer, default=60, server_default="60")
    up_offset: Mapped[int] = mapped_column(Integer, default=10, server_default="10")
    
class DaySettings(BaseModel):
    __tablename__ = "day"

    day_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    start_hour: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=9, server_default="9")
    end_hour: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=21, server_default="21")

class Phones(BaseModel):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    phone: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    viewed: Mapped[bool] = mapped_column(Boolean, index=True, server_default=false())