import uvicorn

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.db import engine, Base, get_db
from app.models.cattle import GenderEnum
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
        if _cattle.gender == GenderEnum.MALE.value:
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

@app.get("/add-cattle-weight/{cattle_id}", response_class=HTMLResponse)
async def add_cattle_weight_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = crud.get_cattle_by_id(db, cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return templates.TemplateResponse("cattle_weight_form.html", {"request": request, "action": "create", "cattle": cattle_data})

@app.get("/cattle-weight-list", response_class=HTMLResponse)
async def cattle_weight_list(request: Request, cattle_id: str = None, db: Session = Depends(get_db)):
    # Convert cattle_id to int or None
    parsed_cattle_id = None
    if cattle_id and cattle_id.strip():
        try:
            parsed_cattle_id = int(cattle_id)
        except ValueError:
            parsed_cattle_id = None
    
    # Buscar todos os animais para o filtro
    cattle_list = crud.get_all_cattle(db)
    
    # Buscar registros de peso (com filtro opcional por cattle_id)
    weight_records = crud.get_all_cattle_weight(db, parsed_cattle_id)

    return templates.TemplateResponse("cattle_weight_list.html", {
        "request": request, 
        "weight_records": weight_records,
        "cattle_list": cattle_list,
        "selected_cattle_id": parsed_cattle_id
    })

@app.get("/edit-cattle-weight/{weight_id}", response_class=HTMLResponse)
async def edit_cattle_weight_form(request: Request, weight_id: int, db: Session = Depends(get_db)):
    # Assumindo que você terá uma função para buscar peso por ID
    # cattle_weight = crud.get_cattle_weight_by_id(db, weight_id)
    # if not cattle_weight:
    #     raise HTTPException(status_code=404, detail="Cattle weight record not found")
    # cattle_data = crud.get_cattle_by_id(db, cattle_weight.cattle_id)
    # return templates.TemplateResponse("cattle_weight_form.html", {"request": request, "action": "edit", "cattle": cattle_data, "cattle_weight": cattle_weight})
    pass

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8008, reload=True)