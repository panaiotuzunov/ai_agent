import os
from google.genai import types


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
    

schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Returns the content of a file, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The path to the file of which the contents should be listed, relative to the working directory.",
            ),
    },
),
)