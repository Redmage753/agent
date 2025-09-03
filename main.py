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
You are a helpful AI coding agent that only gets one reply.

When a user asks a question or makes a request, make a function call plan, and ONLY reply once you've executed the plan and can fully answer the prompt. Only reply with the answer, not your function call plan.
All the information you need can be accessed using the functions - defaults are built in to help, as needed. I recommend you start by listing all directories and their nested directory contents. You can call more than one function in a reply and it will loop through all the contents.

You can perform the following operations:

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

def generate_content(message_chain=[]):
    generated_content = client.models.generate_content(
        model = ai_model, 
        contents = message_chain,
        config = types.GenerateContentConfig(tools=[af.available_functions],system_instruction=system_prompt),
        )
    return generated_content

#def add_message(message_chain, new_message):
#    return message_chain.append(new_message)

def main():
    user_prompts,verbosity=store_prompts()
    for prompt in user_prompts:
        prompting=True
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        while prompting:
            if len(messages) < 20:
                import time
                time.sleep(20)
                response = generate_content(messages)
                if response.text:
                    print(response.text)
                    return
                if verbosity == True:
                    print_verbose(prompt, response)
                for candidate in response.candidates[:]:
                    print(f"Appending messages with {candidate.content}")
                    #messages = add_message(messages, candidate.content)
                    messages.append(candidate.content)
                if response.function_calls:
                    if response.text and response.text.strip():
                        print(response.text)
                    for function in response.function_calls:
                        #print(f"Requesting function: {function.name}({function.args})")
                        function_return_part = cf.call_function(function, verbose=verbosity)
                        print(f"New Message: {messages.append(types.Content(role="user", parts=function_return_part.parts))}")
                        #messages = add_message(messages, types.Content(role="user", parts=function_return_part.parts))
                        #print(f"New Message: {messages}")
            else:
                prompting = False
            #else:
            #    print(response.text)
        #print(f"PRINTING CANDIDATE CONTENT: {response.candidates[0].content}")
        #response = client.models.generate_content(
        #    model = ai_model, 
        #    contents = messages,
        #    config = types.GenerateContentConfig(tools=[af.available_functions],system_instruction=system_prompt),
        #)
        #if verbosity == True:
        #    print_verbose(prompt, response)
        #print(f"Response candidates: {len(response.candidates)}") 
        #print(f"Response contents: {response.candidates}")
        #print(type(response.candidates[0].content.parts))
        #print(response.candidates[0].content.parts[0]) # winner
        #for candidate in response.candidates[:]:
        #    print(f"Appending messages with {candidate.content}")
            #response.contents.messages.append(candidate.content)
            #messages.append(candidate.content)
        #    messages = add_message(messages, candidate.content)
        #print(f"PRINTING CANDIDATE CONTENT: {response.candidates[0].content}")
        #print(f"PRINTING MESSAGE: {response.candidates[0].content}")

        #if response.function_calls:
        #    if response.text and response.text.strip():
        #        print(response.text)
        #    for function in response.function_calls:
        #        #print(f"Requesting function: {function.name}({function.args})")
        #        function_return_part = cf.call_function(function, verbose=verbosity)
        #        messages = add_message(messages, types.Content(role="user", parts=function_return_part.parts))
        #        print(f"New Message: {messages}")
                #print(f"New Message: {messages.append(types.Content(role="user", parts=function_return_part.parts))}")

            #for key,value in function_map.items():
            #    if key in af.available_functions:
       # else:
       #     print(response.text)
        #for item in messages:
        #    print("------")
        #    print(item)

    
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
