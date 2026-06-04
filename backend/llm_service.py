import os
import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Upgraded Pydantic schemas for Hackathon Judge Mode
class IdeaItem(BaseModel):
    title: str = Field(description="Innovative and catchy title of the hackathon project idea")
    description: str = Field(description="Clear explanation of the problem solved, core functionality, and value proposition")
    tech_stack: List[str] = Field(description="A tailored list of technologies, frameworks, libraries, and APIs suitable for the skill level")
    roadmap: List[str] = Field(description="Milestones representing a step-by-step roadmap to complete the demo during the hackathon timeline")
    complexity_score: int = Field(description="Realistic difficulty score from 1 (very basic) to 10 (exceptionally complex)", ge=1, le=10)
    impact_score: int = Field(description="Realistic score evaluating market demand, real-world utility, and demo wow-factor from 1 to 10", ge=1, le=10)

class HackathonIdeasResponse(BaseModel):
    ideas: List[IdeaItem] = Field(description="Exactly 3 diverse project ideas: Idea 1 is AI-centric, Idea 2 is Web/App Platform, Idea 3 is Automation/System tool")
    best_idea_index: int = Field(description="The index (0, 1, or 2) of the most recommended idea in the list", ge=0, le=2)
    ranking_reason: str = Field(description="A brief explanation details why this specific idea ranks best, considering timeline feasibility and hackathon judge impact")

def get_mock_ideas(domain: str, skill_level: str, time_available: int) -> Dict[str, Any]:
    """
    Generates realistic, diverse, and graded mockup ideas when no API key is set.
    Ensures correct schema representation containing best_idea_index and ranking_reason.
    """
    logger.info(f"Using mock fallback generator for domain: {domain}, skill: {skill_level}, time: {time_available}h")
    domain_lower = domain.lower()

    # Base generic templates that adjust complexity by skill level
    diff_shift = 0
    if skill_level == "Beginner":
        diff_shift = -1
    elif skill_level == "Advanced":
        diff_shift = 1

    # Pre-configured specialized domains
    if "health" in domain_lower or "medical" in domain_lower:
        ideas = [
            {
                "title": "MedScribe AI",
                "description": "An AI-centric voice assistant that listens to patient-doctor conversations and generates structured prescription reports and summaries.",
                "tech_stack": ["FastAPI", "Gemini API", "SpeechRecognition", "Tailwind CSS"],
                "roadmap": [
                    "Record raw audio streams via browser micro-interaction",
                    "Transcribe audio and feed to LLM summarizing template",
                    "Render interactive patient summary cards and PDF exporter"
                ],
                "complexity_score": max(1, min(10, 6 + diff_shift)),
                "impact_score": 8
            },
            {
                "title": "VitaTrack Portal",
                "description": "A web/app dashboard visualizing patient vitals, medication timelines, and synchronizing with Google Calendar for alerts.",
                "tech_stack": ["FastAPI", "React", "Google Calendar API", "SQLite"],
                "roadmap": [
                    "Define relational database schemas for vitals and alerts",
                    "Integrate OAuth2 and Google Calendar API sync tasks",
                    "Build dynamic vital metrics chart widgets"
                ],
                "complexity_score": max(1, min(10, 5 + diff_shift)),
                "impact_score": 7
            },
            {
                "title": "PulseGuard Daemon",
                "description": "An automation tool that monitors raw health logs and alerts doctors via SMS if critical metrics show signs of anomaly.",
                "tech_stack": ["FastAPI", "Pandas", "Twilio API", "Redis"],
                "roadmap": [
                    "Create stream ingestion consumer endpoint",
                    "Deploy anomaly detector module based on standard deviation limits",
                    "Configure Twilio SMS critical escalation triggers"
                ],
                "complexity_score": max(1, min(10, 7 + diff_shift)),
                "impact_score": 9
            }
        ]
        best_index = 0
        reason = "MedScribe AI represents the best balance of wow-factor and feasibility. Implementing text summarizing with the Gemini API is straightforward yet highly impressive for hackathon judges."
    
    elif "fin" in domain_lower or "money" in domain_lower or "bank" in domain_lower:
        ideas = [
            {
                "title": "FinSentry AI",
                "description": "An AI-centric transaction monitoring module designed to predict micro-transaction patterns and alert users to fraudulent activities.",
                "tech_stack": ["FastAPI", "Scikit-Learn", "Redis", "HTML/CSS"],
                "roadmap": [
                    "Gather sample banking transaction CSV structures",
                    "Train dynamic outlier detection isolation forest",
                    "Configure Webhook alerting system"
                ],
                "complexity_score": max(1, min(10, 7 + diff_shift)),
                "impact_score": 9
            },
            {
                "title": "ShareSplit Web",
                "description": "A collaborative bill-splitting dashboard designed for shared houses, integrating instant payment links.",
                "tech_stack": ["FastAPI", "Bootstrap", "Stripe API", "PostgreSQL"],
                "roadmap": [
                    "Design house bill groups databases",
                    "Implement Stripe payment link builder APIs",
                    "Create status widgets highlighting balances"
                ],
                "complexity_score": max(1, min(10, 5 + diff_shift)),
                "impact_score": 6
            },
            {
                "title": "StripeAuto Escrow",
                "description": "An automation system handling instant buyer-seller escrow locking via scheduled script run timers.",
                "tech_stack": ["FastAPI", "Apscheduler", "SQLite", "Python"],
                "roadmap": [
                    "Design transaction states database",
                    "Write automatic confirmation schedule triggers",
                    "Create dispute response triggers"
                ],
                "complexity_score": max(1, min(10, 6 + diff_shift)),
                "impact_score": 8
            }
        ]
        best_index = 0
        reason = "FinSentry AI is selected because predictive financial security showcases deep technical intelligence, creating high demo value within the timeline limits."

    elif "edu" in domain_lower or "learn" in domain_lower or "school" in domain_lower:
        ideas = [
            {
                "title": "LingoBot AI",
                "description": "An AI language conversation partner that chats with students and rates grammar and pronoun usage in real-time.",
                "tech_stack": ["FastAPI", "Gemini API", "HTML/CSS", "JavaScript"],
                "roadmap": [
                    "Setup chat interface using static files",
                    "Pipe speech prompts to Gemini structure API",
                    "Parse grammar ratings and suggest corrections"
                ],
                "complexity_score": max(1, min(10, 6 + diff_shift)),
                "impact_score": 8
            },
            {
                "title": "StudyQuest Portal",
                "description": "A gamified web platform converting study syllabus lists into interactive quiz games and badges.",
                "tech_stack": ["FastAPI", "React", "Chart.js", "SQLite"],
                "roadmap": [
                    "Create user scoreboards and level metrics databases",
                    "Set up multiple-choice quiz engines",
                    "Build rewards badges inventory view"
                ],
                "complexity_score": max(1, min(10, 5 + diff_shift)),
                "impact_score": 7
            },
            {
                "title": "ClassAuto Sync",
                "description": "An automation scheduler syncing online classroom lecture recordings to organized cloud storage folders.",
                "tech_stack": ["FastAPI", "Google Drive API", "Apscheduler", "Python"],
                "roadmap": [
                    "Authenticate Drive API workspace integrations",
                    "Build automated folder indexing directory builders",
                    "Develop status notifications daemon"
                ],
                "complexity_score": max(1, min(10, 6 + diff_shift)),
                "impact_score": 6
            }
        ]
        best_index = 0
        reason = "LingoBot AI represents the highest judge utility. Real-time language correction is highly interactive, interactive, and fits cleanly inside a short hackathon schedule."

    else:
        # Fallback dynamic generalized template matching requested domain
        ideas = [
            {
                "title": f"Smart {domain} Agent",
                "description": f"An AI-centric companion assistant automating queries and workflow planning within the {domain} sector.",
                "tech_stack": ["FastAPI", "Gemini API", "HTML/CSS", "SQLite"],
                "roadmap": [
                    "Build API prompt templates tailored to the sector",
                    "Create simple messaging chat interfaces",
                    "Implement query history logging features"
                ],
                "complexity_score": max(1, min(10, 6 + diff_shift)),
                "impact_score": 8
            },
            {
                "title": f"{domain} Hub Portal",
                "description": f"A collaborative web platform designed to map resources and share updates inside the {domain} space.",
                "tech_stack": ["FastAPI", "Tailwind CSS", "SQLite", "Python"],
                "roadmap": [
                    "Design regional assets database schemas",
                    "Implement interactive lists and tag filtering",
                    "Create simple CRUD upload forms"
                ],
                "complexity_score": max(1, min(10, 4 + diff_shift)),
                "impact_score": 6
            },
            {
                "title": f"{domain} Sync Automation",
                "description": f"A background automation service monitoring and formatting data imports in the {domain} pipeline.",
                "tech_stack": ["FastAPI", "Pandas", "APScheduler", "Email API"],
                "roadmap": [
                    "Setup schedule file importers",
                    "Validate CSV schemas with Pandas and format rows",
                    "Build alert mail dispatchers on parsing exceptions"
                ],
                "complexity_score": max(1, min(10, 7 + diff_shift)),
                "impact_score": 7
            }
        ]
        best_index = 0
        reason = f"The Smart {domain} Agent has the highest potential for a hackathon win due to its practical AI integration and immediate demo impact."

    return {
        "ideas": ideas,
        "best_idea_index": best_index,
        "ranking_reason": reason
    }

def generate_ideas(domain: str, skill_level: str, time_available: int) -> Dict[str, Any]:
    """
    Calls the Gemini API using structured JSON mode to generate 3 diverse, ranked hackathon ideas.
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
            "You are HackForge AI, an expert hackathon mentor and professional judge.\n\n"
            f"Generate EXACTLY 3 diverse and unique hackathon project ideas based on the user's constraints:\n"
            f"- Domain: {domain}\n"
            f"- Skill Level: {skill_level}\n"
            f"- Time Available: {time_available} hours\n\n"
            "DIFFERENT TYPE RULE:\n"
            "The 3 generated ideas must represent different technical paradigms to ensure diversity:\n"
            "- Idea 1: AI-centric solution (utilizing LLMs, ML classifiers, agents, etc.)\n"
            "- Idea 2: Interactive Web/App platform (focused on databases, user collaboration, APIs)\n"
            "- Idea 3: Automation/System tool (focused on schedulers, scripts, sync pipelines, background tasks)\n\n"
            "DIFFICULTY CALIBRATION:\n"
            f"Calibrate complexity score to match the '{skill_level}' skill level and the '{time_available}' hours timeframe. "
            "Ensure the roadmaps represent clear steps doable in this timeframe.\n\n"
            "JUDGE SCORING & RANKING:\n"
            "- Provide both a 'complexity_score' (1-10) and an 'impact_score' (1-10) evaluating real-world value.\n"
            "- Rank the ideas. Select the best one and identify its index (0, 1, or 2) in 'best_idea_index'.\n"
            "- Provide a clear reason in 'ranking_reason' justifying why it is the most competitive project.\n\n"
            "Return the ideas strictly conforming to the requested response schema structure. No markdown wrappers."
        )
        
        user_prompt = (
            f"Generate 3 diverse hackathon project ideas for the '{domain}' domain, "
            f"calibrated for '{skill_level}' level to build in {time_available} hours."
        )
        
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
