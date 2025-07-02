import os

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            file_content_str = f.read()

        if len(file_content_str) > 10000:
            with open(abs_file_path, "r") as f:
                file_content_str = f.read(10000)
            file_content_str = file_content_str + f'[...File "{file_path}" truncated at 10000 characters]'
        
        return file_content_str
        
    except Exception as e:
        return f"Error: {str(e)}"
    
