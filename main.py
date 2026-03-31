import os
import json
import vertexai
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, Part
from google.oauth2 import service_account

# ==============================
# 🔧 CONFIG & INITIALIZATION
# ==============================

PROJECT_ID = os.getenv("PROJECT_ID", "gemini-live-agent-489604")
LOCATION = os.getenv("LOCATION", "us-central1")
# Path to your secret key on Vercel/Render
KEY_PATH = "/etc/secrets/key.json" 

try:
    if os.path.exists(KEY_PATH):
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    else:
        # Fallback for local testing if you use an env var instead
        credentials_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "{}"))
        if credentials_info:
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
        else:
            raise ValueError("No Google credentials found at /etc/secrets/key.json or in ENV")

    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    model = GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"CRITICAL INIT ERROR: {e}")

# ==============================
# 🚀 APP INIT & CORS
# ==============================

app = FastAPI(title="Gemini AI Backend", version="2.0")

# Proper CORS setup for separate Vercel hosting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

# ==============================
# 🟢 HEALTH & ROOT
# ==============================

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Gemini Multimodal Backend is Live"}

# ==============================
# 🤖 TEXT AI (/api/ask)
# ==============================

@app.post("/api/ask")
async def ask_ai(q: Question):
    try:
        prompt = f"Answer clearly and concisely: {q.question}"
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("Empty response from Gemini")

        return {"answer": response.text}

    except Exception as e:
        print(f"ERROR /api/ask: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
# 🖼️ IMAGE AI (/api/vision)
# ==============================

@app.post("/api/vision")
async def vision(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await file.read()
        image_part = Part.from_data(mime_type=file.content_type, data=contents)

        response = model.generate_content([
            "Describe what you see in this image briefly for a voice response.",
            image_part
        ])

        return {"analysis": response.text}

    except Exception as e:
        print(f"ERROR /api/vision: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
# ⚡ STREAMING (/api/ask-stream)
# ==============================

@app.post("/api/ask-stream")
async def ask_stream(q: Question):
    try:
        def generate():
            responses = model.generate_content(q.question, stream=True)
            for chunk in responses:
                if chunk.text:
                    yield chunk.text

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        print(f"ERROR /api/ask-stream: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))