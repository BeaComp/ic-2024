import shutil
import magic
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, status

app = FastAPI()

SUPPORTED_FILE_TYPES = {
    'image/png': 'png'
}

@app.post("/upload")
async def upload_image(files: List[UploadFile] = File(...)):
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
        
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"sucess": True, 'file_name': img.filename}