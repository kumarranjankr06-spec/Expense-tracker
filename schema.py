from pydantic import BaseModel,EmailStr
from datetime import datetime
class user(BaseModel):
  name:str
  email:EmailStr
  phone:int
  pass1:str
  pass2:str
  
  
  
class signup(BaseModel):
  email:EmailStr
  pass1:str
  
  
class expense(BaseModel):
  amount:int
  cat:str
  time:datetime
  desc:str