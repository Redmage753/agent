import os

def write_file(working_directory, file_path, content):
    #print(working_directory)
    #print(file_path)
    abs_working_dir=os.path.abspath(working_directory)
    target_file=os.path.abspath(os.path.join(working_directory, file_path))
    #print(abs_working_dir)
    #print(target_file)
    try:
        if not target_file.startswith(abs_working_dir):
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.')
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return (f'Error: {e}')
