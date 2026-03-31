from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Gemini
vertexai.init(project="gemini-live-agent-489604", location="us-central1")

model = GenerativeModel("gemini-2.0-flash")

app = FastAPI()

# CORS configuration (THIS FIXES YOUR ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str


@app.post("/ask")
async def ask_ai(q: Question):
    response = model.generate_content(q.question)
    return {"answer": response.text}


@app.get("/")
def home():
    return {"message": "Gemini backend running"}

from fastapi import UploadFile, File
from vertexai.generative_models import Part

@app.post("/vision")
async def vision_ai(file: UploadFile = File(...)):

    contents = await file.read()

    image_part = Part.from_data(
        mime_type=file.content_type,
        data=contents
    )

    response = model.generate_content([
        "Describe what you see in this image",
        image_part
    ])

    return {"analysis": response.text}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8080)