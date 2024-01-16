# main.py
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Initialize FastAPI app
app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://postgres:admin@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)

# Initialize SQLAlchemy models
Base = declarative_base()

class Example(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Dependency to get the database session
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# FastAPI endpoints
@app.post("/create_item/")
def create_item(item: dict, db: Session = Depends(get_db)):
    db_item = Example(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/get_items/")
def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Example).offset(skip).limit(limit).all()
    return items
