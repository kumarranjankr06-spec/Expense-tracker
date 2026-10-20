from fastapi import FastAPI,Depends,HTTPException,responses,status
from database import create_engine,Base,get_db,sessionmaker,sessionLoad,engine
from schema import user,signup,expense
from auth import hash_password,verify_password,create_access_token,get_current_user
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import session
from models import User,Expense



app=FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)



@app.get("/hello")
def home_page():
  return "hello and welcome to the home page here"

@app.post("/login")
def login_page(asd:user,db:session=Depends(get_db)):
  if asd.pass1==asd.pass2:
    poi=hash_password(asd.pass2)
    z=db.query(User).filter(User.email==asd.email).first()
    z1=db.query(User).filter(User.phone==asd.phone).first()
    if z:
      raise HTTPException(status_code=404,detail="the email id that you have entered alredy exists in the database there")
    if z1:
      raise HTTPException(status_code=404,detail="the phone number that you have entered alredy exists in the database there")
    
    cu=User(name=asd.name,email=asd.email,phone=asd.phone,password=poi)
    db.add(cu)
    db.commit()
    db.refresh(cu)
  return {"data":"the new data have been added in the database"}


@app.post("/signup")
def sign_up(asd:signup,db:session=Depends(get_db)):
  z=db.query(User).filter(User.email==asd.email).first()
  if (z is None or not verify_password(asd.pass1,z.password)): 
    raise HTTPException(status_code=405,detail="the entered email or the password is wrong")
  
  token=create_access_token(z.id)
  
  return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/home")
def home_page(current_user:User=Depends(get_current_user)):
  return {
    "message":"user has logged in succesfuly using jwt",
    "user_id":current_user.id
  }
  
@app.post("/expense")
def expense_page(asd:expense,db:session=Depends(get_db),current_user:User=Depends(get_current_user)):
  exp=Expense(amount=asd.amount,desc=asd.desc,cat=asd.cat,time=asd.time,user_id=current_user.id)
  db.add(exp)
  db.commit()
  db.refresh(exp)
  return {
    "message":"your expense have been added to the database",
    "expense_id":exp.id,
    "user_id":current_user.id,
    "amount":exp.amount
  }
  