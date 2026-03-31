import vertexai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, Part
from fastapi.responses import FileResponse # 👈 NEW IMPORT

# Initialize Gemini
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

# 🟢 FIX: Serve index.html when you visit the main link
@app.get("/")
async def read_index():
    return FileResponse('index.html')

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_ai(q: Question):
    response = model.generate_content(q.question)
    return {"answer": response.text}

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

# 1. Initialize with your specific Project ID
vertexai.init(project="gemini-live-agent-489604", location="us-central1")

print("--- Connecting to Gemini... ---")

# 2. Define the model
model = GenerativeModel("gemini-2.0-flash")

# 3. Generate content and CAPTURE the response
try:
    response = model.generate_content("Explain AI in two lines.")
    
    # 4. CRITICAL: You must print the .text attribute
    print("Response from Gemini:")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

print("--- Script Finished ---")