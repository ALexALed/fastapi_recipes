from http.client import HTTPException
from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse


ud_router = APIRouter()

@ud_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}



@ud_router.get("/downloadfile/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    if not Path(filename).exists():
        raise HTTPException(status_code=404)
    return FileResponse(filename=filename, path=f"uploads/{filename}")