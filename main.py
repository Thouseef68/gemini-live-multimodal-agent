import vertexai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, Part
from fastapi.responses import FileResponse

vertexai.init(project="gemini-live-agent-489604", location="us-central1")
model = GenerativeModel("gemini-2.0-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse('home.html')

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_ai(q: Question):
    # Gemini answers here when you speak!
    response = model.generate_content(q.question)
    return {"answer": response.text}

@app.post("/vision")
async def vision_ai(file: UploadFile = File(...)):
    # Gemini answers here when you use the camera!
    contents = await file.read()
    image_part = Part.from_data(mime_type=file.content_type, data=contents)
    response = model.generate_content(["Describe this image", image_part])
    return {"analysis": response.text}