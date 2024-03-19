import shutil
import magic
import os
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, status

app = FastAPI()

SUPPORTED_FILE_TYPES = {
    'image/png': 'png'
}

@app.post("/upload")
async def upload_image(files: List[UploadFile] = File(...), folder_path: str = 'uploads'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!'
        )
    
    for img in files:
        contents = await img.read()
        file_type = magic.from_buffer(buffer=contents, mime=True)
        if file_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
            )
        
        with open(os.path.join(folder_path, img.filename), "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"success": True, 'file_names': [img.filename for img in files]}
