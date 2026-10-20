from database import Base
from sqlalchemy import String,Integer,Column,BigInteger,DateTime,ForeignKey

class User(Base):
  __tablename__="Users"
  
  id=Column(Integer,nullable=False,primary_key=True,unique=True)
  name=Column(String,nullable=False)
  email=Column(String,nullable=False,unique=True)
  password=Column(String,nullable=False)
  phone=Column(BigInteger,nullable=False,unique=True)
  
  
class Expense(Base):
  __tablename__="Expense"
  
  id=Column(Integer,nullable=False,unique=True,primary_key=True)
  amount=Column(Integer,nullable=False)
  desc=Column(String,nullable=False)
  cat=Column(String,nullable=False)
  time=Column(DateTime,nullable=False)
  user_id = Column(Integer,ForeignKey("Users.id"),nullable=False)