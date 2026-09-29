import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./portace.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    tags = Column(JSON, nullable=False)

    roadmap = relationship("RoadmapModel", back_populates="project", uselist=False)


class RoadmapModel(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True, nullable=False)
    overview = Column(Text, nullable=False)
    prerequisites = Column(JSON, nullable=False)
    daily_breakdown = Column(JSON, nullable=False)
    key_challenges = Column(JSON, nullable=False)

    project = relationship("ProjectModel", back_populates="roadmap")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()