from pathlib import Path
import shutil
import tempfile
from typing import List, Tuple
import json 
from fastapi import FastAPI, UploadFile, HTTPException, status, Query, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Json
# from config import settings # settings is loaded from json inside the function
from utils.io import populate
import uuid 
from datetime import datetime
from database import start_session, close_session, populate_db, get_job_by_status, get_matching_job, cn, cr

app = FastAPI(
    title="MachineACS API",
    description="Text cleaning and processing API",
    version="1.0.0"
)

# Optional: ensure session is started if global cr is None
if not cr and cn:
    start_session()

KIND_MAP = {
    ".json": "json",
    ".jsonl": "jsonl",
    ".csv": "csv",
    ".txt": "txt"
}

UPLOAD_DIR = Path(tempfile.gettempdir()) / "machineacs_uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def serve_file(file_path: Path, filename: str):
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return FileResponse(
        path=file_path, 
        filename=filename, 
        media_type='application/octet-stream',
        content_disposition_type='inline'
    )

@app.get("/")
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the MachineACS API",
        "documentation": "/docs",
        "endpoints": ["/clean"]
    }

@app.post("/clean")
async def clean_files(filtres: List[str] = Query(...), files: List[UploadFile] = File(...)):
    
    results = []

    try:
        with open("config/settings.json", "r") as f:
            settings_data = json.load(f)
    except FileNotFoundError:
        settings_data = {}

    final_config = {"filters": {}}
    for filter_name in filtres:
        if filter_name in settings_data and settings_data[filter_name] is True:
            if filter_name == "newlines":
                final_config["newlines"] = True
            else:
                final_config["filters"][filter_name] = True

    for file in files:
        file_ext = Path(file.filename).suffix.lower()
        kind = KIND_MAP.get(file_ext)

        if kind is None:
            continue

        save_path = UPLOAD_DIR / file.filename

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        entry = (kind, file.filename, str(save_path.absolute()))
        results.append(entry)

    this_job_id = str(uuid.uuid4())
    
    # Initialize job history
    populate_db(this_job_id, "pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Job created, processing {len(results)} files")

    try:
        files_to_process = results
        populate_db(this_job_id, "processing", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Cleaning in progress...")

        files_for_download = await populate(final_config, files_to_process)
        
        populate_db(this_job_id, "completed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Files processed successfully")
        
        if files_for_download and len(files_for_download) > 0:
            # Return the first cleaned file directly
            file_name, file_path_str = files_for_download[0]
            return serve_file(Path(file_path_str), file_name)

    except Exception as e:
        populate_db(this_job_id, "failed", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    # Fallback return message if no files found
    message = get_matching_job(this_job_id)
    return message 

@app.get("/jobs/{status}")
async def get_job(status: str):
    return get_job_by_status(status)

@app.on_event("shutdown")
def shutdown_event():
    close_session()
