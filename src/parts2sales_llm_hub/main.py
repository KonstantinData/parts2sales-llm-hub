"""
main.py — FastAPI WebUI for gpt-pipeline-hub evaluation pipeline
-----------------------------------------------------------------
Serves the UI, triggers background evaluation pipeline runs,
displays summary results, and handles output downloads.
"""

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import subprocess
import json
import logging

from parts2sales_llm_hub.upload_routes import router as upload_router

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path setup (project root: .../parts2sales-llm-hub)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
EVAL_DIR = BASE_DIR / "evals"
SUMMARY_FILE = EVAL_DIR / "pipeline_summary.json"
STATUS_FILE = EVAL_DIR / "status.json"
COST_FILE = EVAL_DIR / "token_costs_summary.json"

# FastAPI app instance
app = FastAPI()

# Mount static files (only if available)
# Mount static files (only if available)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    logger.warning(f"⚠️ Static directory not found: {STATIC_DIR}")

# Mount templates (only if available)
if TEMPLATE_DIR.exists():
    templates = Jinja2Templates(directory=TEMPLATE_DIR)
else:
    logger.warning(f"⚠️ Template directory not found: {TEMPLATE_DIR}")
    templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    summary_data = {}
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, encoding="utf-8") as f:
            summary_data = json.load(f)
    return templates.TemplateResponse(
        "index.html", {"request": request, "summary": summary_data}
    )


@app.post("/run")
def run_pipeline(background_tasks: BackgroundTasks):
    logger.info("🚀 POST /run received")
    background_tasks.add_task(run_all)
    return {"status": "⏳ Evaluation started in background"}


def write_status(step: str):
    STATUS_FILE.write_text(json.dumps({"status": step}))


def run_all():
    logger.info("🔥 run_all() triggered")
    try:
        EVAL_DIR.mkdir(parents=True, exist_ok=True)

        steps = [
            "feature_determination_latest",
            "use_case_determination_latest",
            "industry_classification_latest",
        ]
        for step in steps:
            write_status(f"Running: {step}")
            subprocess.run(
                ["python", "scripts/eval_runner.py", step],
                check=True,
            )

        write_status("Evaluating")
        subprocess.run(
            ["python", "scripts/eval_runner.py", step], check=True, cwd=BASE_DIR
        )

        write_status("Saving")
        subprocess.run(["python", "token_cost_summary.py"], check=True)

        write_status("Providing Downloads")
        write_status("Complete")
        logger.info("🎉 Evaluation pipeline completed.")
    except subprocess.CalledProcessError as e:
        write_status(f"Error: {str(e)}")
        logger.error(f"❌ Subprocess failed: {e}")
    except Exception as e:
        try:
            write_status(f"Error: {str(e)}")
        except Exception as write_err:
            logger.error(f"❌ Failed to write status file: {write_err}")
        logger.exception("⚠️ Unexpected error occurred during evaluation.")


@app.get("/download/{filename}")
def download_result(filename: str):
    file_path = EVAL_DIR / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}


@app.get("/download/latest")
def download_latest_evaluation():
    latest = sorted(EVAL_DIR.glob("evaluation_output_*.json"), reverse=True)
    if not latest:
        return {"error": "No evaluation output available"}
    latest_file = latest[0]
    return FileResponse(
        latest_file,
        media_type="application/json",
        filename=latest_file.name,
        headers={"Content-Disposition": f'attachment; filename="{latest_file.name}"'},
    )


# Optional local run
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("parts2sales_llm_hub.main:app", host="0.0.0.0", port=8000, reload=True)
