from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Define the path to the main folder
main_folder_path = "main"

@app.get("/{file_name}")
async def serve_file(file_name: str):
    # Construct the full path to the file
    file_path = os.path.join(main_folder_path, 'example.txt')
    
    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

