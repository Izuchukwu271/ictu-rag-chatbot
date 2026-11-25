
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

interaction = client.interactions.create(
   model="gemini-3.5-flash-lite",
    input="Reply with exactly: Gemini API test passed."
)

print(interaction.output_text)
