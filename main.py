from typing import List, Optional
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, ProjectModel

app = FastAPI(
    title="PortAce API",
    description="Backend filter engine for PortAce project ideas",
    version="1.0.0"
)

class ProjectSchema(BaseModel):
    id: int
    title: str
    tagline: str
    difficulty: str
    domain: str
    tags: List[str]
    core_concepts: List[str]

    class Config:
        from_attributes = True


@app.get("/")
def health_check():
    return {"status": "online", "app": "PortAce API"}


@app.get("/projects", response_model=List[ProjectSchema])
def get_projects(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    tag: Optional[str] = Query(None, description="Filter by tech stack tag"),
    db: Session = Depends(get_db)
):
    """
    Fetch project ideas with optional filters for difficulty, domain, and tech stack tag.
    """
    query = db.query(ProjectModel)

    if difficulty:
        query = query.filter(ProjectModel.difficulty.ilike(f"%{difficulty}%"))

    if domain:
        query = query.filter(ProjectModel.domain.ilike(f"%{domain}%"))

    projects = query.all()

    if tag:
        filtered_projects = []
        for p in projects:
            if p.tags and any(tag.lower() == t.lower() for t in p.tags):
                filtered_projects.append(p)
        return filtered_projects

    return projects