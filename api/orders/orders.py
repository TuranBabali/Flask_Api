from ..utils import db
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Integer,String, Text,Boolean,DateTime,ForeignKey
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum as SAEnum

class Sizes(PyEnum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

class OrderStatus(PyEnum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'



class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    size: Mapped[Sizes] = mapped_column(SAEnum(Sizes), default=Sizes.SMALL)
    order_status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    flavour: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    quantity: Mapped[int]= mapped_column(Integer())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    customer: Mapped["User"]= relationship("User", back_populates="orders")
    def __repr__(self):
        return f"<Order {self.id}>"
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text(), nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='customer', lazy=True)




    def __repr__(self):
        return f"<User {self.username}>"
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    
        