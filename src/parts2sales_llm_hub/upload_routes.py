"""
upload_routes.py — Upload-Endpunkte für Prompt-Validierung
----------------------------------------------------------
Ermöglicht das Hochladen von YAML- oder JSON-Dateien zur Validierung
und Integration in die Prompt-Pipeline.

Routen:
- POST /upload/prompt: Lädt eine Prompt-Definition hoch
- POST /upload/metadata: Lädt eine Metadaten-Datei hoch
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload/prompt")
async def upload_prompt_file(file: UploadFile = File(...)):
    """
    Lädt eine Prompt-Definitionsdatei hoch und speichert sie im Upload-Verzeichnis.
    """
    if not file.filename.endswith((".yaml", ".yml", ".json")):
        raise HTTPException(
            status_code=400, detail="Nur YAML- oder JSON-Dateien erlaubt."
        )
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"Datei {file.filename} erfolgreich hochgeladen."}


@router.post("/upload/metadata")
async def upload_metadata_file(file: UploadFile = File(...)):
    """
    Lädt eine Metadaten-Datei hoch und speichert sie im Upload-Verzeichnis.
    """
    if not file.filename.endswith((".yaml", ".yml", ".json")):
        raise HTTPException(
            status_code=400, detail="Nur YAML- oder JSON-Dateien erlaubt."
        )
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"Metadaten-Datei {file.filename} erfolgreich hochgeladen."}
