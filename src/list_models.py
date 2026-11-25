from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

print("Models supporting text generation:\n")

for model in client.models.list():
    actions = getattr(model, "supported_actions", []) or []

    if "generateContent" in actions:
        print(model.name)