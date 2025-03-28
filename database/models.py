from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    state = Column(String)
    username = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PaymentMovement(Base):
    __tablename__ = "payment_movements"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, ForeignKey('users.id'))
    generated_link = Column(String)
    payment_type = Column(String)
    total_price = Column(DECIMAL(20, 2))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())