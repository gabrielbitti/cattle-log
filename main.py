import uvicorn

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.db import engine, Base, get_db
from app.routers import cattle
from app import crud, schemas # Import crud and schemas
import os

# Create database tables if they don\\'t exist (Alembic is preferred for production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Auditoria de Rebanho")

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(cattle.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    cow_count = 0
    bull_count = 0

    all_cattle = crud.get_all_cattle(db)
    for _cattle in all_cattle:
        if _cattle.type == "bull":
            bull_count += 1
        else:
            cow_count += 1

    data = dict(
        request=request,
        cattle_count=len(all_cattle),
        cow_count=cow_count,
        bull_count=bull_count,
    )

    return templates.TemplateResponse("index.html", data)

@app.get("/add-cattle", response_class=HTMLResponse)
async def add_cattle_form(request: Request):
    return templates.TemplateResponse("cattle_form.html", {"request": request, "action": "create"})

@app.get("/add-birth", response_class=HTMLResponse)
async def add_birth_form(request: Request):
    return templates.TemplateResponse("add_birth.html", {"request": request})

@app.get("/cattle-list", response_class=HTMLResponse)
async def list_cattle_page(request: Request, db: Session = Depends(get_db)):
    cattle_list = crud.get_all_cattle(db, limit=1000) # Fetch all cattle (adjust limit if needed)
    return templates.TemplateResponse("list_cattle.html", {"request": request, "cattle_list": cattle_list})

@app.get("/cattle/edit/{cattle_id}", response_class=HTMLResponse)
async def edit_cattle_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = crud.get_cattle_by_id(db, cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return templates.TemplateResponse("cattle_form.html", {"request": request, "action": "edit", "cattle": cattle_data})

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8008, reload=True)