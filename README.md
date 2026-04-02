# 🚀 Gemini Live Multimodal Agent

## 🧠 Overview
A real-time multimodal AI agent capable of understanding and responding using vision, voice, and text.

Built using Google Gemini and deployed on Google Cloud, this system demonstrates next-generation human-AI interaction.

---

## 🔥 Key Features

### 🎤 Voice Interaction
- Real-time voice input using browser speech recognition  

### 👁️ Vision Understanding
- Processes live webcam input for image analysis  

### 🔄 Live Vision Mode
- Continuous real-time scene understanding  

### 🔊 Speech Output
- AI responses converted to speech  

### ☁️ Cloud Deployment
- Deployed on Google Cloud Run  
- Integrated with Vertex AI (Gemini)  

---

## 🏗️ Architecture

User (Voice + Camera)  
↓  
Frontend (HTML + JavaScript)  
↓  
Backend (FastAPI - Cloud Run)  
↓  
Vertex AI (Gemini Model)  
↓  
AI Response (Text + Speech)  

---

## 🛠️ Tech Stack

### Frontend
- HTML  
- JavaScript  
- Web Speech API  
- Web Camera API  

### Backend
- Python  
- FastAPI  

### Cloud
- Google Cloud Run  
- Vertex AI (Gemini)  

---

## 🌐 Live Deployment
🔗 https://gemini-live-agent-74863738813.us-central1.run.app  

---

## ⚙️ Run Locally

```bash
pip install -r requirements.txt
uvicorn backend:app --reload
```

Open `index.html` in your browser.

---

## 🎥 Demo
https://vimeo.com/1179532580?fl=ip&fe=ec

---

## 🏆 Hackathon Project
Built for the Gemini Live Agent Challenge Hackathon.

---

## 🚀 Future Improvements
- Better UI/UX  
- Conversational memory  
- Mobile optimization  
- Real-time object tracking  

---

## 💡 Impact
Demonstrates how multimodal AI systems can enable natural human-computer interaction using real-time data.

---
