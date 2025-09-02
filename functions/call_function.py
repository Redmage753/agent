import os
from google.genai import types
import traceback
from functions.run_python import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

FUNCTIONS = {
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "get_file_content": get_file_content,
    "write_file": write_file,
    }

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {name}({kwargs})")
    else:
        print(f" - Calling function: {name}")

    func = FUNCTIONS.get(name)
    if not func:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=name, response={"error": f"Unknown function: {name}"}
            )],
        )
    result = func(**kwargs)

    if verbose:
        print(f"-> {{'result': {result}}}")

    print(f"About to call: {func.__module__}.{func.__name__}")
    print(f"kwargs: {kwargs}")
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=name, response={"result": result}
        )],
    )
'''
    function=function_call_part
    try:
        if type(function.args) != dict and type(function.name) != str:
            raise "Error: Not a function call."
        function.args["directory"] = "./calculator"
        #Debugging statements
        print("args:")
        print(type(function.args))
        print("name:")
        print(type(function.name))
        for part in function:
            print(f"Part={part}")
        if verbose:
            print(f"Calling function: {function.name}({function.args})")
        else:
            print(f" - Calling function: {function.name}")
        return run_python_file('functions', f"{function.name}.py", {**function.args})
    except Exception as e:
        print("exception!")
        #print(f'File: {__file__}')
        #print(type(function.name))
        print(f'{__file__} pError: {e}')
        traceback.print_exc()
        return f'{__file__} rError: {e}'
    #working_dir="./calculator"

    #result=f'{function.name}({working_dir}, **{(str(function.args))})'
    #print(f'result: {result}')
        
        #function_map={
        #    function.name: function.args
        #    }
        
        #return function.name(**function.args)}"]
        #response = f'{result}'
        #response
        #result=function.name(working_dir, **function.args)
        #print(f"result: {type(result)} type and value is {result}")
        #new_function[function.name]=new_function[function.args]
        #print(f"NF: {type(new_function)} type and value is {new_function}")
        #print(f"NF: {type(new_function.args)} type and value is {new_function.args}")
        #return function[function.name]**(function[function.args])
        #return function.name(**function.args)
'''
