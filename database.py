from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy.orm import session

load_dotenv()

url=os.getenv("url")
print(url)
engine=create_engine(url)
sessionLoad=sessionmaker(bind=engine , autoflush=False , autocommit=False)

Base=declarative_base()
def get_db():
  db=sessionLoad()
  try:
    yield db
  finally:
    db.close()
