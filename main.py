import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

ai_model = "gemini-2.0-flash-001"
user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

# Using a file example
#file = client.files.upload(file='a11.txt')
#response = client.models.generate_content(
#    model='gemini-2.0-flash-001',
#    contents=['Could you summarize this file?', file]
#)
#print(response.text)
# https://googleapis.github.io/python-genai/#generate-content



def main():
    response = client.models.generate_content(model = ai_model, contents = user_prompt)
    print(response.text)
	print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")
    #print("Hello from agent!")


if __name__ == "__main__":
    main()
