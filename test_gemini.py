import vertexai
from vertexai.generative_models import GenerativeModel

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