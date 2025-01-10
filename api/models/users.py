from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Text, Boolean



from ..utils import db



class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int]= mapped_column(Integer,primary_key=True)
    username: Mapped[str]= mapped_column(String(45),nullable=False, unique=True)
    email: Mapped[str]= mapped_column(String(45),nullable=False, unique=True)
    password_hash: Mapped[str]= mapped_column(Text(),nullable=False)
    is_staff: Mapped[bool]= mapped_column(Boolean(), default=False)
    is_active: Mapped[bool]= mapped_column(Boolean(), default=False)
    
    orders= db.relationship('Order',backref='customer',lazy= True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()