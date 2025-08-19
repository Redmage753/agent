import os

def get_files_info(working_directory, directory="."):
    joined_path=os.path.join(working_directory, directory)
    absolute_working_dir = os.path.abspath(working_directory) # better solution
    target_dir = os.path.abspath(os.path.join(working_directory, directory)) # better solution/naming
    try:
        if not target_dir.startswith(absolute_working_dir):
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(joined_path):
            return (f'Error: "{directory}" is not a directory')
        else:
            contents=os.listdir(joined_path)
            table_list=[]
            table_string=""
            for item in contents:
                table_list.append(f"- {item}: file_size={os.path.getsize(os.path.join(joined_path, item))} bytes, is_dir={os.path.isdir(os.path.join(joined_path, item))}")
            table_string = "\n".join(table_list)
            return table_string
    except Exception as e:
        print(f"Error: {e}")
        return

