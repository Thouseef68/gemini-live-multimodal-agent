#!/bin/bash

# Deploy Gemini Live Multimodal Agent to Google Cloud Run

PROJECT_ID=gemini-live-agent-489604
SERVICE_NAME=gemini-live-agent
REGION=us-central1

gcloud config set project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --allow-unauthenticated
