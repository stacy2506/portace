# PortAce 

**PortAce** is an AI-powered CS project generator and 7-day execution roadmap engine built with FastAPI, SQLAlchemy, and Google Gemini 2.5 Flash.

## Features
- **Project Discovery:** Filter CS project ideas by domain (`Web Dev`, `AI/ML`, `Systems`), difficulty, and tech stack.
- **AI Roadmap Generator:** Generates structured 7-day technical roadmaps enforcing strict JSON output via Pydantic schemas.
- **Customized Roadmaps:** Generates tailored roadmaps based on user constraints (hours per day, skill level, preferred libraries).
- **SQLite Database Caching:** Persists generated roadmaps to minimize Gemini API latency and costs.

## Tech Stack
- **Backend:** Python 3.12, FastAPI, Uvicorn
- **Database:** SQLite & SQLAlchemy ORM
- **AI Integration:** Google Gemini API (`google-genai` SDK)
- **Containerization:** Docker & Docker Compose

## Quickstart

### Local Setup
```bash
# Clone repository
git clone [https://github.com/stacy2506/portace.git](https://github.com/stacy2506/portace.git)
cd portace

# Set up environment variables (.env)
echo "GEMINI_API_KEY=your_gemini_api_key" > .env

# Run backend server
uvicorn main:app --reload

