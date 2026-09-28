from sqlalchemy import create_engine, Column, Integer, String, Text, JSON  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  

DATABASE_URL = "sqlite:///./portace.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    tagline = Column(Text)
    difficulty = Column(String, index=True)  
    domain = Column(String, index=True)      
    tags = Column(JSON)                      
    core_concepts = Column(JSON)            


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

