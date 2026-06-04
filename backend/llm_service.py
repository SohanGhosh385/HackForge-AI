import os
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Setup simple logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Pydantic schemas for Gemini Structured Output
class IdeaItem(BaseModel):
    title: str = Field(description="Title of the hackathon project idea")
    description: str = Field(description="Clear explanation of the project concept and features")
    tech_stack: List[str] = Field(description="List of technologies, frameworks, and APIs to use")
    roadmap: List[str] = Field(description="Step-by-step milestones to build the project during the hackathon")
    complexity_score: int = Field(description="Complexity score from 1 to 10", ge=1, le=10)

class HackathonIdeasResponse(BaseModel):
    ideas: List[IdeaItem] = Field(description="Exactly 3 hackathon project ideas")

def get_mock_ideas(domain: str, skill_level: str, time_available: int) -> Dict[str, Any]:
    """
    Generates realistic mockup data for demonstration when no API key is provided.
    """
    logger.info(f"Using mock fallback generator for domain: {domain}, skill: {skill_level}, time: {time_available}h")
    
    domain_lower = domain.lower()
    
    # Pre-configured domains
    if "health" in domain_lower or "medical" in domain_lower:
        return {
            "ideas": [
                {
                    "title": "MedReminder AI",
                    "description": "An automated SMS/email reminder system using NLP to parse doctor prescriptions and alert patients.",
                    "tech_stack": ["FastAPI", "Twilio API", "SQLite", "HTML/CSS"],
                    "roadmap": [
                        "Parse image or text of prescriptions",
                        "Configure Twilio reminder scheduler",
                        "Build patient dashboard UI"
                    ],
                    "complexity_score": 5 if skill_level == "Beginner" else 4
                },
                {
                    "title": "SymptomCheck Bot",
                    "description": "A lightweight AI chatbot that triage user symptoms and suggests matching OTC drugs or doctor consultations.",
                    "tech_stack": ["FastAPI", "HuggingFace Transformers", "React", "MongoDB"],
                    "roadmap": [
                        "Train classifier on symptoms dataset",
                        "Create WebSocket API for chat streaming",
                        "Deploy responsive chatbot UI"
                    ],
                    "complexity_score": 7 if skill_level == "Intermediate" else 6
                },
                {
                    "title": "AeroTrack AR",
                    "description": "A web application that visualizes indoor air quality and pollen alerts in near real-time.",
                    "tech_stack": ["FastAPI", "Leaflet.js", "OpenWeatherMap API", "PostgreSQL"],
                    "roadmap": [
                        "Aggregate air quality index APIs",
                        "Build geospatial mapping frontend",
                        "Implement alert notifications engine"
                    ],
                    "complexity_score": 8 if skill_level == "Advanced" else 6
                }
            ]
        }
    elif "fin" in domain_lower or "money" in domain_lower or "bank" in domain_lower:
        return {
            "ideas": [
                {
                    "title": "MicroSplit",
                    "description": "A payment app designed to split subscription bills automatically among roommates.",
                    "tech_stack": ["FastAPI", "Stripe API", "SQLite", "Bootstrap"],
                    "roadmap": [
                        "Create subscription grouping endpoints",
                        "Integrate Stripe split-payment webhook",
                        "Build room management interface"
                    ],
                    "complexity_score": 5 if skill_level == "Beginner" else 4
                },
                {
                    "title": "BudgetBuddy AI",
                    "description": "An AI assistant that analyzes CSV statements and generates personalized saving plans.",
                    "tech_stack": ["FastAPI", "Pandas", "Gemini API", "Chart.js"],
                    "roadmap": [
                        "Build CSV statement uploader backend",
                        "Parse and categorize transactions with Pandas",
                        "Render data visualization charts"
                    ],
                    "complexity_score": 7 if skill_level == "Intermediate" else 5
                },
                {
                    "title": "CryptoShield",
                    "description": "A real-time anomaly detection pipeline alerting users to suspicious transfers in Web3 wallets.",
                    "tech_stack": ["FastAPI", "Web3.py", "Redis", "Etherscan API"],
                    "roadmap": [
                        "Connect to blockchain nodes via Web3.py",
                        "Compute transaction moving averages",
                        "Send real-time alerts via WebSockets"
                    ],
                    "complexity_score": 9 if skill_level == "Advanced" else 7
                }
            ]
        }
    else:
        # Generic Template fallback
        return {
            "ideas": [
                {
                    "title": f"Smart {domain} Navigator",
                    "description": f"A web portal helping users navigate {domain} challenges using intelligent categorization.",
                    "tech_stack": ["FastAPI", "Tailwind CSS", "SQLite", "Python"],
                    "roadmap": [
                        "Design database schema",
                        "Implement filter APIs",
                        "Construct simple visual tables"
                    ],
                    "complexity_score": 4 if skill_level == "Beginner" else 3
                },
                {
                    "title": f"{domain} Hub AI",
                    "description": f"An automated generator of {domain} workflows customized for {skill_level} developers.",
                    "tech_stack": ["FastAPI", "Gemini API", "React", "PostgreSQL"],
                    "roadmap": [
                        "Integrate basic LLM wrapper",
                        "Build responsive workflow builder UI",
                        "Implement user history save features"
                    ],
                    "complexity_score": 7 if skill_level == "Intermediate" else 5
                },
                {
                    "title": f"{domain} Sentinel",
                    "description": f"An advanced monitoring agent checking {domain} data streams for anomalies and predicting failures.",
                    "tech_stack": ["FastAPI", "Scikit-Learn", "Redis", "WebSockets"],
                    "roadmap": [
                        "Train ML outlier detector model",
                        "Integrate stream ingestion consumer",
                        "Create real-time notification push system"
                    ],
                    "complexity_score": 9 if skill_level == "Advanced" else 7
                }
            ]
        }

def generate_ideas(domain: str, skill_level: str, time_available: int) -> Dict[str, Any]:
    """
    Calls the Gemini API using structured JSON mode to generate 3 hackathon ideas.
    If the API key is missing or invalid, falls back to realistic mock ideas.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Check if API key is present and not the default example placeholder
    if not api_key or api_key.strip() == "" or "your_gemini_api_key" in api_key.lower():
        logger.info("GEMINI_API_KEY environment variable is missing or placeholder. Running in Offline Mock mode.")
        return get_mock_ideas(domain, skill_level, time_available)
        
    try:
        from google import genai
        from google.genai import types
        
        logger.info("Initializing Google GenAI client...")
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are HackForge AI, an expert hackathon mentor.\n\n"
            f"Generate EXACTLY 3 hackathon project ideas based on the user's constraints:\n"
            f"- Domain: {domain}\n"
            f"- Skill Level: {skill_level}\n"
            f"- Time Available: {time_available} hours\n\n"
            "Each idea must include:\n"
            "- title\n"
            "- description\n"
            "- tech_stack (list of strings)\n"
            "- roadmap (list of steps/milestones)\n"
            "- complexity_score (an integer between 1 and 10)\n\n"
            "Return the ideas strictly conforming to the requested response schema structure."
        )
        
        user_prompt = f"Please generate 3 hackathon ideas for the '{domain}' domain tailored to the '{skill_level}' skill level to build in {time_available} hours."
        
        logger.info(f"Sending request to gemini-2.5-flash for domain: {domain}")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=HackathonIdeasResponse,
                temperature=0.7,
            ),
        )
        
        # Parse output text into standard JSON dict
        if response.text:
            parsed_data = json.loads(response.text)
            logger.info("Successfully received structured response from Gemini.")
            return parsed_data
        else:
            raise ValueError("Empty response text from LLM.")
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}. Falling back to mock generator.")
        return get_mock_ideas(domain, skill_level, time_available)
import json
