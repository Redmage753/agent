import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    #print(f"{file_path} test")
    #print(f"{working_directory} test")
    abs_working_dir=os.path.abspath(working_directory)
    target_file_path=os.path.abspath(os.path.join(working_directory, file_path))
    #print(f"{abs_working_dir} abs_work_dir")
    #print(f"{target_file_path} target_path")
    try:
        if not target_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        #result=subprocess.run([f"cd {abs_working_dir}",f"uv run {target_file_path} ${args}"], timeout=30, capture_output=True)
        #if not args==[]:
        commands = ["python", target_file_path]
        if args:
            commands.extend(args)
        result= subprocess.run(
        commands,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=abs_working_dir
        )
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        return "\n".join(output_parts) if output_parts else "No output produced."
        #    result=subprocess.run([f"uv run {target_file_path} {args}"], timeout=30, capture_output=True, shell=True, text=True)
        #else:
        #    result=subprocess.run([f"uv run {target_file_path}"], timeout=30, capture_output=True, shell=True, text=True)
        #for key,value in vars(result).items():
        #    if value:
        #        print(f"{key}: {value}")
        #if not result:
        #    return f'No output produced.'
        #exit_code=""
        #if not result.returncode==0:
        #    exit_code=f'Process exited with code {result.returncode}'
        #return f'STDOUT:\n{str(result.stdout)}\nSTDERR:\n{str(result.stderr)}\n{exit_code}' 

    except Exception as e:
        return f'Error: executing Python file: {e}'
