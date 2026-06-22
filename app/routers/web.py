import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.cattle import GenderEnum
from app.repositories.cattle import CattleRepository
from app.repositories.cattle_health import CattleHealthRepository
from app.repositories.cattle_weight import CattleWeightRepository

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../../templates"))

router = APIRouter(
    tags=["Web"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    all_cattle = CattleRepository(db).get_all()
    cow_count = sum(1 for c in all_cattle if c.gender == GenderEnum.FEMALE)
    bull_count = sum(1 for c in all_cattle if c.gender == GenderEnum.MALE)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "cattle_count": len(all_cattle),
        "cow_count": cow_count,
        "bull_count": bull_count,
    })


@router.get("/add-cattle", response_class=HTMLResponse)
async def add_cattle_form(request: Request):
    return templates.TemplateResponse("cattle_form.html", {"request": request, "action": "create"})


@router.get("/add-birth", response_class=HTMLResponse)
async def add_birth_form(request: Request):
    return templates.TemplateResponse("add_birth.html", {"request": request})


@router.get("/cattle-list", response_class=HTMLResponse)
async def list_cattle_page(request: Request, db: Session = Depends(get_db)):
    cattle_list = CattleRepository(db).get_all(limit=1000)
    return templates.TemplateResponse("list_cattle.html", {"request": request, "cattle_list": cattle_list})


@router.get("/cattle/edit/{cattle_id}", response_class=HTMLResponse)
async def edit_cattle_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = CattleRepository(db).get_by_id(cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return templates.TemplateResponse("cattle_form.html", {"request": request, "action": "edit", "cattle": cattle_data})


@router.get("/add-cattle-weight/{cattle_id}", response_class=HTMLResponse)
async def add_cattle_weight_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = CattleRepository(db).get_by_id(cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return templates.TemplateResponse("cattle_weight_form.html", {"request": request, "action": "create", "cattle": cattle_data})


@router.get("/cattle-weight-list", response_class=HTMLResponse)
async def cattle_weight_list(request: Request, cattle_id: str = None, db: Session = Depends(get_db)):
    parsed_cattle_id = None
    if cattle_id and cattle_id.strip():
        try:
            parsed_cattle_id = int(cattle_id)
        except ValueError:
            pass

    repo = CattleWeightRepository(db)
    cattle_list = CattleRepository(db).get_all()
    weight_records = repo.get_all_by_cattle(parsed_cattle_id) if parsed_cattle_id else repo.get_all()

    return templates.TemplateResponse("cattle_weight_list.html", {
        "request": request,
        "weight_records": weight_records,
        "cattle_list": cattle_list,
        "selected_cattle_id": parsed_cattle_id,
    })


@router.get("/edit-cattle-weight/{weight_id}", response_class=HTMLResponse)
async def edit_cattle_weight_form(request: Request, weight_id: int, db: Session = Depends(get_db)):
    cattle_weight_details = CattleWeightRepository(db).get_by_id(weight_id)
    if not cattle_weight_details:
        raise HTTPException(status_code=404, detail="Cattle weight record not found")
    cattle_data = CattleRepository(db).get_by_id(cattle_weight_details.cattle_id)
    return templates.TemplateResponse("cattle_weight_form.html", {
        "request": request,
        "action": "edit",
        "cattle": cattle_data,
        "cattle_weight": cattle_weight_details,
    })


@router.get("/add-cattle-health/{cattle_id}", response_class=HTMLResponse)
async def add_cattle_health_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = CattleRepository(db).get_by_id(cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return templates.TemplateResponse("cattle_health_form.html", {"request": request, "action": "create", "cattle": cattle_data})


@router.get("/cattle-health-list", response_class=HTMLResponse)
async def cattle_health_list(request: Request, cattle_id: str = None, db: Session = Depends(get_db)):
    parsed_cattle_id = None
    if cattle_id and cattle_id.strip():
        try:
            parsed_cattle_id = int(cattle_id)
        except ValueError:
            pass

    repo = CattleHealthRepository(db)
    cattle_list = CattleRepository(db).get_all()
    health_records = repo.get_all_by_cattle(parsed_cattle_id) if parsed_cattle_id else repo.get_all()

    return templates.TemplateResponse("cattle_health_list.html", {
        "request": request,
        "health_records": health_records,
        "cattle_list": cattle_list,
        "selected_cattle_id": parsed_cattle_id,
    })


@router.get("/edit-cattle-health/{health_id}", response_class=HTMLResponse)
async def edit_cattle_health_form(request: Request, health_id: int, db: Session = Depends(get_db)):
    cattle_health_details = CattleHealthRepository(db).get_by_id(health_id)
    if not cattle_health_details:
        raise HTTPException(status_code=404, detail="Cattle health record not found")
    cattle_data = CattleRepository(db).get_by_id(cattle_health_details.cattle_id)
    return templates.TemplateResponse("cattle_health_form.html", {
        "request": request,
        "action": "edit",
        "cattle": cattle_data,
        "cattle_health": cattle_health_details,
    })


@router.get("/health")
def health_check():
    return {"status": "ok"}
