import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
#from functions.get_files_info import schema_get_files_info
#from functions.get_files_info import available_functions
import functions.available_functions as af
import functions.call_function as cf

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
ai_model = "gemini-2.0-flash-001"
system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
""" 

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
#    print(f"Full Response: {response}")

def main():
    user_prompts,verbosity=store_prompts()
    for prompt in user_prompts:
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        response = client.models.generate_content(
            model = ai_model, 
            contents = messages,
            config = types.GenerateContentConfig(tools=[af.available_functions],system_instruction=system_prompt),
        )
        if verbosity == True:
            print_verbose(prompt, response)
        if response.function_calls:
            if response.text and response.text.strip():
                print(response.text)
            for function in response.function_calls:
                print(f"Calling function: {function.name}({function.args})")
                print(cf.call_function(function, verbose=True))
        else:
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
