import os, subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    _, ext = os.path.splitext(file_path)
    if ext != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, cwd=abs_working_dir, text=True)
        result_str = f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}\n'
        if result.returncode != 0:
            result_str += f"Process exited with code {result.returncode}\n"
        if result.stdout == "" and result.stderr == "":
            result_str += "No output produced.\n"
        return result_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
