# Gemini Live Multimodal Agent

A real-time AI assistant that can **see, hear, and speak** using Google's Gemini model and Google Cloud.

This project was created for the **Gemini Live Agent Challenge Hackathon**.

---

# Project Overview

Gemini Live Multimodal Agent is an AI system that allows users to interact with an intelligent assistant using **voice commands and real-time camera input**.

The agent can:

• Listen to voice commands
• Analyze images from a webcam
• Generate intelligent responses using Gemini
• Speak responses back to the user
• Run live vision analysis continuously

---

# Key Features

### Voice Interaction

Users can speak directly to the AI assistant using browser voice recognition.

### Vision Analysis

The system captures webcam frames and sends them to Gemini for image understanding.

### Live Vision Mode

The AI continuously analyzes the camera feed and provides real-time explanations.

### Speech Output

AI responses are spoken using browser speech synthesis.

### Cloud Deployment

The backend is deployed on **Google Cloud Run** and communicates with **Vertex AI Gemini**.

---

# Architecture

User (Camera + Voice)
↓
Web Interface (HTML + JavaScript)
↓
Cloud Run Backend (FastAPI)
↓
Vertex AI (Gemini Model)
↓
AI Response (Text + Speech)

---

# Tech Stack

Frontend
• HTML
• JavaScript
• Web Speech API
• Web Camera API

Backend
• FastAPI
• Python

Cloud
• Google Cloud Run
• Vertex AI (Gemini)

---

# Google Cloud Deployment

Backend Service URL:

https://gemini-live-agent-74863738813.us-central1.run.app

---

# Running the Project Locally

1. Install Python dependencies

pip install -r requirements.txt

2. Start the backend

uvicorn backend:app --reload

3. Open the frontend

Open `index.html` in your browser.

---

# Demo Video

Demo video submitted as part of the hackathon.

---

# Hackathon Submission

This project was built for the **Gemini Live Agent Challenge** to demonstrate multimodal AI interaction combining:

• Voice
• Vision
• Real-time reasoning
• Cloud AI services

---

# Future Improvements

• Enhanced UI animations
• More intelligent conversational memory
• Mobile compatibility
• Real-time object tracking
