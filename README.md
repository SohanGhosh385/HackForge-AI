                    ┌────────────────────────────┐
                    │        FRONTEND UI         │
                    │ (Static HTML / JS / UI)    │
                    └────────────┬───────────────┘
                                 │ HTTP Request
                                 ▼
                    ┌────────────────────────────┐
                    │      FASTAPI BACKEND       │
                    │  (API Gateway Layer)       │
                    └────────────┬───────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼

┌───────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ Prompt Engine  │     │ Response Parser  │     │ Validation Layer   │
│ (Core Logic)   │     │ (JSON Formatter) │     │ (Schema Check)     │
└──────┬────────┘     └─────────┬────────┘     └─────────┬──────────┘
       │                        │                        │
       └──────────────┬─────────┴──────────────┬────────┘
                      ▼                        ▼
        ┌────────────────────────────────────────────┐
        │          LLM API LAYER                    │
        │ (OpenAI / Gemini / Claude)               │
        └────────────────────────────────────────────┘
                      │
                      ▼
        ┌────────────────────────────────────────────┐
        │        STRUCTURED OUTPUT ENGINE            │
        │  - JSON formatting                        │
        │  - Idea ranking                           │
        │  - Scoring system                         │
        └────────────────────────────────────────────┘
                      │
                      ▼
        ┌────────────────────────────────────────────┐
        │          FINAL RESPONSE API               │
        └────────────────────────────────────────────┘
                      │
                      ▼
                FRONTEND DISPLAY
# HackForge AI – AI Hackathon Idea Generator (MVP)

HackForge AI is a lightweight, single-page GenAI-powered web application that generates tailored hackathon project ideas using LLMs. Designed as a clean, minimal MVP (Minimum Viable Product), it helps students or hackathon participants generate actionable ideas based on their domain of interest, skill level, and available hacking hours.

---

## 🏗️ SYSTEM ARCHITECTURE

```text
  [ Frontend (Static Page) ] 
             │
             ▼ (fetch POST /generate-ideas)
   [ FastAPI Backend (app.py) ]
             │
             ▼ (Pydantic Validation & Prompt Rendering)
  [ LLM Service (llm_service.py) ]
             │
             ▼ (JSON Mode API Call)
     [ Gemini / OpenAI API ]
```

---

## 📁 FOLDER STRUCTURE

```text
hackforge-ai/
├── backend/
│   ├── app.py                # FastAPI server, endpoints, and validation schemas
│   ├── llm_service.py        # LLM integration and system prompt configuration
│   ├── requirements.txt      # Backend dependencies (fastapi, uvicorn, pydantic, google-genai)
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── index.html            # User interface structure
│   ├── style.css             # Basic styling and layout
│   └── script.js             # Form handler and fetch API calls
└── README.md                 # Project documentation and setup guide
```

---

## 🔌 API CONTRACT

### **POST** `/generate-ideas`
* **Request Body:**
```json
{
  "domain": "Healthcare",
  "skill_level": "Intermediate",
  "time_available": 48
}
```

* **Response Body (JSON):**
```json
[
  {
    "title": "MedReminder AI",
    "description": "An automated SMS/email reminder system using NLP to parse doctor prescriptions.",
    "tech_stack": ["FastAPI", "Twilio API", "SQLite", "HTML/CSS"],
    "roadmap": [
      "Set up prescription image/text parser endpoint",
      "Configure Twilio SMS reminder cron-job",
      "Build basic client dashboard"
    ],
    "complexity_score": 6
  }
]
```

---

## 🧠 LLM LOGIC & PROMPTING
The `llm_service.py` defines the system instruction:
> "You are an experienced hackathon mentor. Generate exactly 3 unique project ideas for the domain '{domain}' at a '{skill_level}' skill level to be completed in '{time_available}' hours. Return the ideas strictly conforming to the requested JSON array structure."

---

## 🚀 GETTING STARTED (3-MINUTE SETUP)

### 1. Run the Backend
1. Open a terminal in `backend/`.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file containing your API key:
   ```env
   GEMINI_API_KEY=your-api-key-here
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`.

### 2. Run the Frontend
* Open `frontend/index.html` directly in any web browser or use a simple static server (e.g., Live Server in VS Code).
