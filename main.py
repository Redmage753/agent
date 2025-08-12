import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
ai_model = "gemini-2.0-flash-001"

def store_prompts():
	verbosity = False
	try:
		sys.argv[1] == True
	except Exception as e:
		print(f"No user input provided. Please provide a prompt. see also: {e}")
		sys.exit(1)
	else:
		args_no_flags=list(sys.argv[1:])
		for index,arg in enumerate(args_no_flags):
			if arg == '--verbose':
				args_no_flags.pop(index)
				verbosity=True
		return (args_no_flags, verbosity)

def print_verbose(user_prompt, response):	
	print(f"User prompt: {user_prompt}")
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():
	user_prompts,verbosity=store_prompts()
	for prompt in user_prompts:
		messages = [
			types.Content(role="user", parts=[types.Part(text=prompt)]),
		]
		response = client.models.generate_content(
			model = ai_model, 
			contents = messages
		)
		if verbosity == True:
			print_verbose(prompt, response)
		print(response.text)
	

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
