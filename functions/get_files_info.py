import os

def get_files_info(working_directory, directory="."):
    #print(f"Work_dir: {working_directory}")
    #print(f"Dir: {directory}")
    joined_path=os.path.join(working_directory, directory)
    #print(f"Trying: {joined_path}")
    #print(f"What's the absolute path? {os.path.abspath(directory)}")
    #print(f"is {joined_path} in {os.path.abspath(directory)}?")
    #print(f"Okay..... does it start with my /var/? {str(os.path.abspath(directory))}")
    print(f"Trying true or false:{os.path.abspath(directory).startswith('/var/home/cmander/workspace/github.com/redmage753/agent')} ")
    
    #print(f"Is it a path? {os.path.isdir(joined_path)}")

    try:
        #if not os.path.samepath(joined_path, os.path.abspath(directory):
        if str(os.path.abspath(directory)).startswith('/var/home/cmander/workspace/github.com/redmage753/agent') == False:
            Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(joined_path):
            Exception(f'Error: "{directory}" is not a directory')
        else:
            contents=os.listdir(joined_path)
            print(contents)
    except Exception as e:
        print(f"Error encountered: {e}")
        return
    #contents = os.listdir(joined_path)
    #print(contents)
