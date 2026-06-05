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
    Ensures complete differentiation of project concepts between Beginner, Intermediate, and Advanced tiers.
    """
    logger.info(f"Using mock fallback generator for domain: {domain}, skill: {skill_level}, time: {time_available}h")
    domain_lower = domain.lower()

    # Domain: HEALTHCARE
    if "health" in domain_lower or "medical" in domain_lower:
        if skill_level == "Beginner":
            ideas = [
                {
                    "title": "FitStart Dashboard",
                    "description": "A simple static dashboard where users can input and track their daily calorie intake and water consumption using local storage.",
                    "tech_stack": ["HTML", "CSS", "JavaScript (Vanilla)", "Local Storage"],
                    "roadmap": [
                        "Build semantic calorie log input form",
                        "Design clean local storage data persistency layers",
                        "Construct visual progress charts displaying targets reached"
                    ],
                    "complexity_score": 3,
                    "impact_score": 5
                },
                {
                    "title": "MedCatalog API",
                    "description": "A basic FastAPI search index catalog that allows users to lookup OTC drugs, side effects, and precautions from a static database.",
                    "tech_stack": ["FastAPI", "SQLite", "Python", "HTML"],
                    "roadmap": [
                        "Design flat-file relational SQLite database matching drugs dataset",
                        "Expose simple search GET route with query filters",
                        "Build minimal frontend query browser cards"
                    ],
                    "complexity_score": 3,
                    "impact_score": 4
                },
                {
                    "title": "WaterLogger Scheduler",
                    "description": "A scheduled background script that pushes browser notifications to remind users to drink water and hydrate based on predefined hourly intervals.",
                    "tech_stack": ["HTML5 Notifications API", "JavaScript", "CSS"],
                    "roadmap": [
                        "Request desktop alert permissions in browser",
                        "Configure standard browser notification setInterval timers",
                        "Design settings dashboard to adjust alert frequencies"
                    ],
                    "complexity_score": 2,
                    "impact_score": 5
                }
            ]
            best_index = 0
            reason = "FitStart Dashboard is selected as the top beginner pick because visual calorie logs demonstrate the highest end-user utility while remaining strictly within the capability limits."

        elif skill_level == "Intermediate":
            ideas = [
                {
                    "title": "MedReminder AI",
                    "description": "An AI-centric voice and text helper that parses unstructured prescription images to trigger scheduled medication SMS alerts using third-party APIs.",
                    "tech_stack": ["FastAPI", "Gemini API", "Twilio API", "SQLite"],
                    "roadmap": [
                        "Create image upload endpoint for prescriptions",
                        "Pipe text segments to LLM to parse times and medications",
                        "Configure Twilio SMS reminder dispatch triggers"
                    ],
                    "complexity_score": 6,
                    "impact_score": 8
                },
                {
                    "title": "VitalMonitor Web",
                    "description": "A collaborative patient dashboard charting real-time vitals and synchronizing appointments directly with Google Calendar.",
                    "tech_stack": ["FastAPI", "React", "Google Calendar API", "PostgreSQL"],
                    "roadmap": [
                        "Implement vitals ingestion and storage tables",
                        "Configure OAuth2 secure connection to Google Calendar",
                        "Build visual charts plotting vital history"
                    ],
                    "complexity_score": 6,
                    "impact_score": 7
                },
                {
                    "title": "PollenAlert System",
                    "description": "An automated background scraper checking air quality levels in specific zip codes and sending automated email warnings.",
                    "tech_stack": ["FastAPI", "OpenWeatherMap API", "SMTP Email API", "Python"],
                    "roadmap": [
                        "Setup location geographic lookup API endpoints",
                        "Deploy ZIP code air index checks hourly",
                        "Format and dispatch automated email alert templates"
                    ],
                    "complexity_score": 5,
                    "impact_score": 6
                }
            ]
            best_index = 0
            reason = "MedReminder AI is selected because parsing prescriptions with LLM extracts impressive tech points from judges while keeping setup time under the limit."

        else: # Advanced
            ideas = [
                {
                    "title": "MedScribe Agentic Hub",
                    "description": "A multi-agent healthcare hub that captures doctor-patient conversation streams, transcribes dialogue, summarizes diagnostics, and formats SOC2-compliant charts.",
                    "tech_stack": ["FastAPI", "LangChain", "Gemini API", "WebSockets", "Redis"],
                    "roadmap": [
                        "Setup WebSocket streams to ingest raw audio dialogues",
                        "Deploy agent workflows translating jargon and summarizing clinical history",
                        "Generate structured medical summary models"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                },
                {
                    "title": "AeroTrack AR Dashboard",
                    "description": "A complex multi-service vital routing dashboard consolidating streaming health data from multiple IoT nodes and warning emergency systems.",
                    "tech_stack": ["FastAPI", "React", "MQTT broker", "Docker", "PostgreSQL"],
                    "roadmap": [
                        "Containerize services into Docker nodes",
                        "Configure MQTT brokers to route sensor streams",
                        "Build real-time websocket monitoring graphs"
                    ],
                    "complexity_score": 8,
                    "impact_score": 8
                },
                {
                    "title": "Anomaly Escaler Pipeline",
                    "description": "An automated ML diagnostics pipeline analyzing streaming vital statistics logs and pushing critical escalations using anomaly classification algorithms.",
                    "tech_stack": ["FastAPI", "Scikit-Learn", "Apache Kafka", "Redis", "Twilio API"],
                    "roadmap": [
                        "Build streaming consumer nodes using Apache Kafka",
                        "Train outlier classification models using isolation forests",
                        "Deploy automated Twilio webhook escalation nodes"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                }
            ]
            best_index = 0
            reason = "MedScribe Agentic Hub is selected. Transcribing and categorizing medical consultation logs using multi-agent frameworks demonstrates outstanding innovation and system depth."

    # Domain: FINTECH
    elif "fin" in domain_lower or "money" in domain_lower or "bank" in domain_lower:
        if skill_level == "Beginner":
            ideas = [
                {
                    "title": "SpendTracker CRUD",
                    "description": "A simple budget tool helping students log daily expenses, categorize transactions, and check their remaining balance using local variables.",
                    "tech_stack": ["HTML", "CSS", "JavaScript (Vanilla)"],
                    "roadmap": [
                        "Construct transactional form fields",
                        "Apply inline array updates saving items in memories",
                        "Expose dynamic total calculators"
                    ],
                    "complexity_score": 3,
                    "impact_score": 5
                },
                {
                    "title": "CoinRate API Wrapper",
                    "description": "A basic FastAPI wrapper that fetches current exchange rates from a public endpoint and formats conversions for travel users.",
                    "tech_stack": ["FastAPI", "Python", "HTTPX", "HTML"],
                    "roadmap": [
                        "Setup exchange rate routes requesting public feeds",
                        "Build simple inputs conversion calculator pages",
                        "Expose formatted JSON results endpoints"
                    ],
                    "complexity_score": 3,
                    "impact_score": 4
                },
                {
                    "title": "Wallet Escrow Scheduler",
                    "description": "A mock transfer transaction runner demonstrating wallet updates after verification validations.",
                    "tech_stack": ["JavaScript", "HTML", "CSS"],
                    "roadmap": [
                        "Build mock buyer/seller account dashboards",
                        "Trigger timed balance reductions on escrow clicks",
                        "Display success notification states"
                    ],
                    "complexity_score": 2,
                    "impact_score": 4
                }
            ]
            best_index = 0
            reason = "SpendTracker CRUD is selected because client-side transaction logs offer immediate feedback and complete functionality with simple code."

        elif skill_level == "Intermediate":
            ideas = [
                {
                    "title": "BudgetBuddy AI Assistant",
                    "description": "An AI financial assistant that parses statements from uploaded bank CSVs, categorizes transaction records, and builds saving summaries.",
                    "tech_stack": ["FastAPI", "Pandas", "Gemini API", "React"],
                    "roadmap": [
                        "Setup CSV upload endpoints",
                        "Parse data tables with Pandas and summarize profiles",
                        "Use LLM to categorize items and suggest budgeting plans"
                    ],
                    "complexity_score": 6,
                    "impact_score": 8
                },
                {
                    "title": "ShareSplit Collaborative Web",
                    "description": "A bill-splitting web platform with collaborative dashboard rooms and Stripe split payment links.",
                    "tech_stack": ["FastAPI", "Stripe API", "PostgreSQL", "Bootstrap"],
                    "roadmap": [
                        "Design group ledger and account tables",
                        "Configure Stripe custom payment link creation",
                        "Construct status dials showing balances owed"
                    ],
                    "complexity_score": 6,
                    "impact_score": 7
                },
                {
                    "title": "StripeAuto Escrow System",
                    "description": "A automated escrow validation worker ensuring payments release after verified timelines.",
                    "tech_stack": ["FastAPI", "APScheduler", "SQLite", "Python"],
                    "roadmap": [
                        "Design transaction state database models",
                        "Build scheduled checks processing pending releases",
                        "Expose user approval API portals"
                    ],
                    "complexity_score": 5,
                    "impact_score": 7
                }
            ]
            best_index = 0
            reason = "BudgetBuddy AI Assistant is selected because AI categorization of raw bank statements offers high demo value and utilizes modern GenAI hooks."

        else: # Advanced
            ideas = [
                {
                    "title": "FinSentry AI Agent",
                    "description": "An advanced AI transaction pipeline analyzing micro-transactions using isolation forest algorithms and automatically flagging suspicious entities.",
                    "tech_stack": ["FastAPI", "Scikit-Learn", "Redis", "Kafka", "WebSockets"],
                    "roadmap": [
                        "Build ingestion stream pipelines using Apache Kafka",
                        "Deploy scikit-learn anomaly classifiers",
                        "Push real-time alert signals via websockets"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                },
                {
                    "title": "WealthFlow Ledgers",
                    "description": "A high-throughput distributed transactional ledger featuring double-entry validation, caching layers, and transaction logs.",
                    "tech_stack": ["FastAPI", "PostgreSQL", "Redis", "Docker", "React"],
                    "roadmap": [
                        "Design secure PostgreSQL transaction tables with locking",
                        "Implement Redis write-back transaction queues",
                        "Build real-time performance logging dashboards"
                    ],
                    "complexity_score": 8,
                    "impact_score": 8
                },
                {
                    "title": "Arbitrage AutoBot",
                    "description": "A microservice scheduler tracking rates across exchange portals and executing cross-wallet arbitrage deals.",
                    "tech_stack": ["FastAPI", "Celery", "Redis", "Web3.py", "Docker"],
                    "roadmap": [
                        "Setup rate scrapers tracking liquidity pools",
                        "Build Celery tasks checking arbitrage margin targets",
                        "Implement mock Web3 wallet signatures pipelines"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                }
            ]
            best_index = 0
            reason = "FinSentry AI Agent is selected. Spotting fraudulent micro-transactions using machine learning models is highly impressive and represents advanced system design."

    # Domain: GENERAL / OTHER
    else:
        if skill_level == "Beginner":
            ideas = [
                {
                    "title": f"{domain} Log CRUD",
                    "description": f"A simple client-side directory page logging {domain} requirements and saving items locally.",
                    "tech_stack": ["HTML", "CSS", "JavaScript"],
                    "roadmap": [
                        "Construct input form layouts",
                        "Design data logging functions",
                        "Expose dynamic metrics totals"
                    ],
                    "complexity_score": 3,
                    "impact_score": 5
                },
                {
                    "title": f"{domain} Finder API",
                    "description": f"A FastAPI lookup tool returning structured dictionary results for the {domain} industry.",
                    "tech_stack": ["FastAPI", "Python", "HTML"],
                    "roadmap": [
                        "Setup dictionary datasets matching domain queries",
                        "Build simple search parameters route",
                        "Implement dynamic template cards"
                    ],
                    "complexity_score": 3,
                    "impact_score": 4
                },
                {
                    "title": f"{domain} Timer Script",
                    "description": "A basic script sending triggers to clean old file logs.",
                    "tech_stack": ["Python", "HTML5"],
                    "roadmap": [
                        "Build setting layouts adjusting timelines",
                        "Configure clean scripts scanning folders",
                        "Display success notification messages"
                    ],
                    "complexity_score": 2,
                    "impact_score": 4
                }
            ]
            best_index = 0
            reason = f"{domain} Log CRUD is selected as it represents a fully operational user utility built with minimal dependencies."

        elif skill_level == "Intermediate":
            ideas = [
                {
                    "title": f"Smart {domain} Agent",
                    "description": f"An AI-centric helper assisting queries and categorizing logs inside the {domain} sector.",
                    "tech_stack": ["FastAPI", "Gemini API", "SQLite", "HTML/CSS"],
                    "roadmap": [
                        "Design database schema tracking query records",
                        "Setup Gemini API connection parsing prompts",
                        "Expose clean chat message interface cards"
                    ],
                    "complexity_score": 6,
                    "impact_score": 8
                },
                {
                    "title": f"{domain} Hub Portal",
                    "description": f"A collaborative web dashboard sharing assets and logs inside the {domain} workspace.",
                    "tech_stack": ["FastAPI", "React", "PostgreSQL", "Tailwind CSS"],
                    "roadmap": [
                        "Build asset sharing databases and tables",
                        "Create CRUD dashboard layouts and files uploader",
                        "Expose user comments and feeds engines"
                    ],
                    "complexity_score": 6,
                    "impact_score": 7
                },
                {
                    "title": f"{domain} Sync Automation",
                    "description": f"A background automation service monitoring format parsing templates in the {domain} pipeline.",
                    "tech_stack": ["FastAPI", "Pandas", "APScheduler", "Email API"],
                    "roadmap": [
                        "Setup file check directories",
                        "Deploy Pandas table parsing and validator rules",
                        "Configure notification emails on exceptions"
                    ],
                    "complexity_score": 5,
                    "impact_score": 7
                }
            ]
            best_index = 0
            reason = f"Smart {domain} Agent is selected because embedding the Gemini API provides excellent value with simple backend code."

        else: # Advanced
            ideas = [
                {
                    "title": f"Smart {domain} Orchestrator",
                    "description": f"An advanced multi-agent pipeline executing automated tasks in the {domain} pipeline using planning loops.",
                    "tech_stack": ["FastAPI", "LangChain", "Gemini API", "Redis", "React"],
                    "roadmap": [
                        "Build worker agent modules tracking subtasks",
                        "Deploy planning routers coordinating actions",
                        "Expose websocket channels showing agent thought trees"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                },
                {
                    "title": f"{domain} Cluster Portal",
                    "description": f"A complex microservices system routing sensor logs across clustered {domain} nodes.",
                    "tech_stack": ["FastAPI", "Docker", "RabbitMQ", "PostgreSQL", "React"],
                    "roadmap": [
                        "Setup service topologies inside Docker containers",
                        "Configure message brokers routing telemetry logs",
                        "Expose real-time websocket metrics graphs"
                    ],
                    "complexity_score": 8,
                    "impact_score": 8
                },
                {
                    "title": f"{domain} Stream anomaly",
                    "description": f"An automated pipeline consuming raw {domain} log streams, parsing parameters, and predicting failures using anomaly detection.",
                    "tech_stack": ["FastAPI", "Kafka", "Scikit-Learn", "Redis", "SMTP API"],
                    "roadmap": [
                        "Setup streaming topics in Kafka",
                        "Deploy ML anomaly classifiers calculating metrics",
                        "Configure SMS/Email notification nodes on alert triggers"
                    ],
                    "complexity_score": 9,
                    "impact_score": 9
                }
            ]
            best_index = 0
            reason = f"Smart {domain} Orchestrator is selected. Building multi-agent workflows executing domain tasks showcases highly impressive system-level design."

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
            "You are HackForge AI, a world-class hackathon mentor, startup incubator judge, and senior AI systems designer.\n\n"
            "Your job is to generate EXACTLY 3 highly distinct hackathon project ideas based on user constraints.\n\n"
            "---\n\n"
            "# 🎯 INPUTS\n\n"
            f"- Domain: {domain}\n"
            f"- Skill Level: {skill_level}\n"
            f"- Time Available: {time_available} hours\n\n"
            "---\n\n"
            "# ⚠️ CRITICAL REQUIREMENT (VERY IMPORTANT)\n\n"
            "The output MUST strongly vary based on skill level.\n\n"
            "If skill_level changes, the ideas MUST NOT overlap in complexity, architecture, or depth.\n\n"
            "---\n\n"
            "# 🧠 SKILL LEVEL BEHAVIOR RULES\n\n"
            "## 🟢 Beginner\n"
            "- Very simple applications\n"
            "- CRUD-based apps or API wrappers\n"
            "- No complex architecture\n"
            "- Minimal AI usage (if any)\n"
            "- Can be built in a few steps\n\n"
            "## 🟡 Intermediate\n"
            "- Multi-component systems (frontend + backend)\n"
            "- API integrations (AI, cloud, or third-party services)\n"
            "- Moderate system design\n"
            "- Real-world usability\n\n"
            "## 🔴 Advanced\n"
            "- Complex system design\n"
            "- Multi-service architecture or agent-based systems\n"
            "- AI-driven workflows or automation pipelines\n"
            "- Scalable, production-like thinking\n"
            "- Innovation-heavy ideas\n\n"
            "---\n\n"
            "# 🚨 DIVERSITY RULE (STRICT)\n\n"
            "Each of the 3 ideas MUST be fundamentally different:\n\n"
            "- Idea 1 → AI-based system\n"
            "- Idea 2 → Web application / platform\n"
            "- Idea 3 → Automation tool / system / infrastructure solution\n\n"
            "No repetition of concepts or domain overlap.\n\n"
            "---\n\n"
            "# 🧠 QUALITY RULES\n\n"
            "- Avoid generic ideas (e.g., to-do apps, basic chatbots)\n"
            "- Ensure ideas are realistic for hackathons\n"
            "- Optimize for feasibility + innovation balance\n"
            "- Respect time_available strictly\n\n"
            "---\n\n"
            "# 🏆 HACKATHON JUDGE MODE\n\n"
            "Act like a strict hackathon judge.\n\n"
            "You should:\n"
            "- Reject weak ideas internally\n"
            "- Prefer practical but impressive ideas\n"
            "- Ensure each idea feels like a “winning project”\n\n"
            "---\n\n"
            "# 📦 OUTPUT FORMAT (STRICT JSON ONLY)\n\n"
            "Return ONLY valid JSON matching the requested schema. NO markdown, NO explanation, NO extra text."
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
