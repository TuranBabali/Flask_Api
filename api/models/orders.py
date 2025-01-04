from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Text, Boolean
from enum import Enum
from datetime import datetime

from..utils import db

class Sizes(Enum):
    SMALL= 'small'
    MEDIUM ='medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

class OrderStatus(Enum):
    PENDING= 'pending'
    IN_TRANSIT= 'in-transit'
    DELIVERED= 'delivered'


class Order(db.Model):
    __tablename__ = 'orders'
    #id: Mapped[int]= mapped_column(Integer, primary_key=True)
    id= db.Column(db.Integer(), primary_key=True)
    size= db.Column(db.Enum(Sizes), default= Sizes.SMALL)
    order_status= db.Column(db.Enum(OrderStatus), default= OrderStatus.PENDING)
    flavour= db.Column(db.String(),nullable= False) 
    date_created= db.Column(db.DateTime(),default=datetime.utcnow) 
    user= db.Column(db.Integer(), db.ForeignKey('users.id'))
                    
    def __repr__(self):
        return f'<Order {self.id}>' 