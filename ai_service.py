import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class DayPlan(BaseModel):
    day: int = Field(description="Day number from 1 to 7")
    title: str = Field(description="Daily focus topic")
    deliverables: list[str] = Field(description="2 to 3 technical deliverables")


class StructuredRoadmap(BaseModel):
    overview: str = Field(description="2-sentence architectural summary")
    prerequisites: list[str] = Field(description="Required tools or libraries prior to Day 1")
    daily_breakdown: list[DayPlan] = Field(description="7 daily execution steps")
    key_challenges: list[str] = Field(description="2 technical hurdles or edge cases")


def generate_project_roadmap(title: str, domain: str, difficulty: str, tags: list[str]) -> StructuredRoadmap:
    prompt = f"""
    You are an expert Senior Software Engineer and Tech Mentor.
    Generate a 7-day execution roadmap for the following CS project:

    Title: {title}
    Domain: {domain}
    Difficulty: {difficulty}
    Tech Stack: {', '.join(tags)}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StructuredRoadmap,
        ),
    )

    return StructuredRoadmap.model_validate_json(response.text)