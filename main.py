from typing import Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db, ProjectModel, RoadmapModel
from ai_service import generate_project_roadmap

app = FastAPI(title="PortAce API", version="1.0")


class ProjectSchema(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    domain: str
    tags: list[str]

    class Config:
        from_attributes = True


class CustomRoadmapRequest(BaseModel):
    hours_per_day: Optional[int] = Field(None, ge=1, le=12, description="Dedicated hours per day")
    preferred_stack: Optional[list[str]] = Field(None, description="Additional tools/libraries")
    user_experience: Optional[str] = Field(None, description="e.g. Beginner, CS Student, Senior Dev")


@app.get("/")
def root():
    return {"message": "PortAce API is running!"}


@app.get("/projects", response_model=list[ProjectSchema])
def get_projects(
    difficulty: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ProjectModel)

    if difficulty:
        query = query.filter(ProjectModel.difficulty.ilike(difficulty))
    if domain:
        query = query.filter(ProjectModel.domain.ilike(domain))

    projects = query.all()

    if tag:
        projects = [p for p in projects if p.tags and tag.lower() in [t.lower() for t in p.tags]]

    return projects


@app.post("/projects/{project_id}/roadmap")
def get_roadmap_for_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_roadmap = db.query(RoadmapModel).filter(RoadmapModel.project_id == project_id).first()
    if existing_roadmap:
        return {
            "source": "database_cache",
            "project_id": project.id,
            "title": project.title,
            "roadmap": {
                "overview": existing_roadmap.overview,
                "prerequisites": existing_roadmap.prerequisites,
                "daily_breakdown": existing_roadmap.daily_breakdown,
                "key_challenges": existing_roadmap.key_challenges,
            }
        }

    roadmap_data = generate_project_roadmap(
        title=project.title,
        domain=project.domain,
        difficulty=project.difficulty,
        tags=project.tags or []
    )

    new_roadmap = RoadmapModel(
        project_id=project.id,
        overview=roadmap_data.overview,
        prerequisites=roadmap_data.prerequisites,
        daily_breakdown=[day.model_dump() for day in roadmap_data.daily_breakdown],
        key_challenges=roadmap_data.key_challenges
    )
    db.add(new_roadmap)
    db.commit()

    return {
        "source": "gemini_generated",
        "project_id": project.id,
        "title": project.title,
        "roadmap": roadmap_data.model_dump()
    }


@app.post("/projects/{project_id}/roadmap/custom")
def get_custom_roadmap(
    project_id: int,
    payload: CustomRoadmapRequest,
    db: Session = Depends(get_db)
):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    roadmap_data = generate_project_roadmap(
        title=project.title,
        domain=project.domain,
        difficulty=project.difficulty,
        tags=project.tags or [],
        hours_per_day=payload.hours_per_day,
        preferred_stack=payload.preferred_stack,
        user_experience=payload.user_experience
    )

    return {
        "source": "gemini_custom_generated",
        "project_id": project.id,
        "title": project.title,
        "customization": payload.model_dump(),
        "roadmap": roadmap_data.model_dump()
    }