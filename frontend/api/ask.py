import json
import os
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel

def handler(request):
    try:
        body = json.loads(request.body)
        question = body.get("question")

        # Load credentials from env
        credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

        credentials = service_account.Credentials.from_service_account_info(credentials_info)

        vertexai.init(
            project="gemini-live-agent-489604",
            location="us-central1",
            credentials=credentials
        )

        model = GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(question)

        return {
            "statusCode": 200,
            "body": json.dumps({"answer": response.text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }