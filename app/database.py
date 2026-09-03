import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from urllib.parse import quote_plus

load_dotenv()

username=os.getenv("DB_USERNAME")
password=quote_plus(os.getenv("DB_PASSWORD",""))
host=os.getenv("DB_HOST","localhost")
database=os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

if __name__=="__main__":
    try:
        with engine.connect()as connection:
            print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed:")
        print(e)