import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

ai_model = "gemini-2.0-flash-001"
#user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
user_prompt = []

def store_prompts():
	try:
		sys.argv[1] == True
	except Exception as e:
		print(f"No user input provided. Please provide a prompt. see also: {e}")
		sys.exit(1)
	else:
		return list(sys.argv[1:])

def main():

	#response = client.models.generate_content(model = ai_model, contents = user_prompt)
	#print(response.text)
	#print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	#print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
	user_prompt=store_prompts()
	for prompt in user_prompt:
		response = client.models.generate_content(model = ai_model, contents = prompt)
		print(response.text)
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
	#	print(i)
	#print(user_prompt)

if __name__ == "__main__":
    main()

# Using a file example
#file = client.files.upload(file='a11.txt')
#response = client.models.generate_content(
#    model='gemini-2.0-flash-001',
#    contents=['Could you summarize this file?', file]
#)
#print(response.text)
# https://googleapis.github.io/python-genai/#generate-content
