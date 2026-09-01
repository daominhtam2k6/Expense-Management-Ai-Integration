from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import models
from app.core.schema_migrations import (
    ensure_category_icon_column,
    ensure_goal_completion_columns,
    ensure_user_profile_columns,
)
from app.database import Base, engine
from app.routers import assistant, auth, budgets, categories, dashboard, goals, reports, transactions


Base.metadata.create_all(bind=engine)
ensure_category_icon_column(engine)
ensure_goal_completion_columns(engine)
ensure_user_profile_columns(engine)

app = FastAPI(title="Expense Management API")

API_PREFIX = "/api"
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
UPLOAD_ROOT = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(categories.router, prefix=API_PREFIX)
app.include_router(transactions.router, prefix=API_PREFIX)
app.include_router(budgets.router, prefix=API_PREFIX)
app.include_router(goals.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(assistant.router, prefix=API_PREFIX)


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    """Serve the built React app and preserve client-side routes on port 8000."""
    if full_path == "api" or full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    index_file = FRONTEND_DIST / "index.html"
    if not index_file.is_file():
        raise HTTPException(
            status_code=503,
            detail="Frontend has not been built. Run `npm.cmd run build` in the frontend directory.",
        )

    requested_file = (FRONTEND_DIST / full_path).resolve()
    try:
        requested_file.relative_to(FRONTEND_DIST.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc

    if full_path and requested_file.is_file():
        return FileResponse(requested_file)

    return FileResponse(index_file, headers={"Cache-Control": "no-store"})
