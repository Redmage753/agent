from google.genai import types

from functions.run_python import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = "./calculator"

    function_map = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "get_file_content": get_file_content,
        "write_file": write_file,
        }

    if verbose:
        print(f"Calling function: {name}({kwargs})")
    else:
        print(f" - Calling function: {name}")

    func = function_map.get(name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name, 
                    response={"error": f"Unknown function: {name}"}
            )],
        )

    result = func(**kwargs)

    if verbose:
        print(f"-> {{'result': {result}}}")

    #print(f"About to call: {func.__module__}.{func.__name__}")
    #print(f"kwargs: {kwargs}")
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=name, response={"result": result}
            )],
        )
