from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from llm_service import generate_ideas, HackathonIdeasResponse

app = FastAPI(
    title="HackForge AI API",
    description="API for the HackForge AI Hackathon Idea Generator (MVP)",
    version="1.0.0"
)

# Enable CORS for local frontend integration (allows loading index.html directly from local system)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for input validation
class IdeaRequest(BaseModel):
    domain: str = Field(..., description="The hackathon domain or industry (e.g. Fintech, Healthcare)")
    skill_level: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="Developer skill level")
    time_available: int = Field(..., description="Time limit for the hackathon in hours", gt=0)

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Domain must be a non-empty string")
        return stripped

# Pydantic schema for health check
class HealthResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to ensure server is running.
    """
    return {"status": "ok"}

@app.post("/mock-ideas", response_model=HackathonIdeasResponse)
def get_mock_ideas_endpoint(request: IdeaRequest):
    """
    Returns mock ideas instantly (under 5 milliseconds) to allow the frontend to render ideas instantly.
    """
    try:
        from llm_service import get_mock_ideas
        mock_response = get_mock_ideas(
            domain=request.domain,
            skill_level=request.skill_level,
            time_available=request.time_available
        )
        return mock_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mock ideas: {str(e)}")

@app.post("/generate-ideas", response_model=HackathonIdeasResponse)
def generate_hackathon_ideas(request: IdeaRequest):
    """
    Primary endpoint that accepts user constraints and returns exactly 3 ideas in JSON format.
    """
    try:
        ideas_response = generate_ideas(
            domain=request.domain,
            skill_level=request.skill_level,
            time_available=request.time_available
        )
        return ideas_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate hackathon ideas: {str(e)}")
