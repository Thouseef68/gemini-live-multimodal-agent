import os
import vertexai
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, Part
from pathlib import Path

# ==============================
# 🔧 CONFIG
# ==============================

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
MODEL_NAME = "gemini-2.0-flash"

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set")

from google.oauth2 import service_account
import vertexai

credentials = service_account.Credentials.from_service_account_file(
    "/etc/secrets/key.json"
)

vertexai.init(
    project="gemini-live-agent-489604",
    location="us-central1",
    credentials=credentials
)

# ==============================
# 🚀 APP INIT
# ==============================

app = FastAPI(title="Gemini AI Backend", version="2.0")

from fastapi import Request
from fastapi.responses import JSONResponse

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )
# ==============================
# 📦 MODELS
# ==============================

class Question(BaseModel):
    question: str

# ==============================
# 🟢 ROUTES
# ==============================

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Backend is running"}

# ==============================
# 🤖 TEXT AI
# ==============================

@app.post("/ask")
async def ask_ai(q: Question):
    try:
        prompt = f"""
        You are a helpful AI assistant.
        Answer clearly and concisely.

        Question: {q.question}
        """

        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("Empty response from model")

        return {"answer": response.text}

    except Exception as e:
        print("ERROR /ask:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ⚡ STREAMING
# ==============================

@app.post("/ask-stream")
async def ask_stream(q: Question):
    try:
        def generate():
            responses = model.generate_content(q.question, stream=True)
            for chunk in responses:
                if chunk.text:
                    yield chunk.text

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        print("ERROR /ask-stream:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# 🖼️ IMAGE AI
# ==============================

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await file.read()

        image_part = Part.from_data(
            mime_type=file.content_type,
            data=contents
        )

        response = model.generate_content([
            "Describe this image in detail",
            image_part
        ])

        return {"analysis": response.text}

    except Exception as e:
        print("ERROR /vision:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# 📄 FILE ANALYSIS
# ==============================

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        file_part = Part.from_data(
            mime_type=file.content_type,
            data=contents
        )

        response = model.generate_content([
            "Summarize this file",
            file_part
        ])

        return {"result": response.text}

    except Exception as e:
        print("ERROR /analyze:", str(e))
        raise HTTPException(status_code=500, detail=str(e))