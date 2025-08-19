import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
			type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),  
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of the file, constrained to the working directory and truncating after 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
			type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
			"file_path": types.Schema(
			type=types.Type.STRING,
			description="The file to list content from, relative to the working directory. If not provided or not a standard file, returns an error.",
			),
        },
    ),  
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python specific file, with arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
			type=types.Type.STRING,
            description="The director to run files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
			"file_path": types.Schema(
			type=types.Type.STRING,
			description="The python file to run, relative to the working directory. Will error if the file is not found, not a python file, or not in the correct directory.",
			),
			"args": types.Schema(
			type=types.Type.STRING,
			description="A string of a list of arguments to provide for the python file being run.",
			),
        },
    ),  
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
			type=types.Type.STRING,
            description="The directory to file writes will be constrained to, relative to the working directory.",
            ),
			"file_path": types.Schema(
			type=types.Type.STRING,
			description="The file to write content to. It will create folders as needed. Constrained to the working directory.",
			),
			"content": types.Schema(
			type=types.Type.STRING,
			description="The contents to be written to the file_path.",
			),
        },
    ),  
)

available_functions = types.Tool(
    function_declarations = [
        schema_get_files_info,
		schema_get_file_content,
		schema_run_python_file,
		schema_write_file
        ]
    )

