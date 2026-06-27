import datetime
import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.domain.cattle_domain import CattleDomain
from app.models.cattle import GenderEnum
from app.repositories.cattle import CattleRepository
from app.repositories.cattle_health import CattleHealthRepository
from app.repositories.cattle_reproduction import CattleReproductionRepository
from app.repositories.cattle_weight import CattleWeightRepository

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../../templates"))


def _status_pt(value) -> str:
    labels = {
        "ACTIVE": "Ativo",
        "SOLD": "Vendido",
        "DECEASED": "Falecido",
        "TRANSFERRED": "Transferido",
    }
    key = value.value if hasattr(value, "value") else str(value)
    return labels.get(key, key)


def _format_date(value) -> str:
    if not value:
        return "-"
    return value.strftime("%d/%m/%Y")


def _event_type_pt(value) -> str:
    labels = {
        "MATING": "Cobertura",
        "PREGNANCY_CHECK": "Diag. Prenhez",
        "BIRTH": "Parto",
        "ABORTION": "Aborto",
        "WEANING": "Desmame",
    }
    key = value.value if hasattr(value, "value") else str(value)
    return labels.get(key, key)


templates.env.filters["status_pt"] = _status_pt
templates.env.filters["format_date"] = _format_date
templates.env.filters["event_type_pt"] = _event_type_pt

router = APIRouter(
    tags=["Web"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    all_cattle = CattleRepository(db).get_all()
    cow_count = sum(1 for c in all_cattle if c.gender == GenderEnum.FEMALE)
    bull_count = sum(1 for c in all_cattle if c.gender == GenderEnum.MALE)

    current_year = datetime.date.today().year
    domain = CattleDomain(db)
    births_by_month = domain.get_births_by_month(current_year)
    births_this_year = sum(births_by_month["male"]) + sum(births_by_month["female"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "cattle_count": len(all_cattle),
        "cow_count": cow_count,
        "bull_count": bull_count,
        "births_by_month": births_by_month,
        "births_this_year": births_this_year,
        "current_year": current_year,
    })


@router.get("/add-cattle", response_class=HTMLResponse)
async def add_cattle_form(request: Request):
    return templates.TemplateResponse("cattle_form.html", {"request": request, "action": "create"})


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


@router.get("/cattle-reproduction-list", response_class=HTMLResponse)
async def cattle_reproduction_list(request: Request, cattle_id: str = None, db: Session = Depends(get_db)):
    parsed_cattle_id = None
    if cattle_id and cattle_id.strip():
        try:
            parsed_cattle_id = int(cattle_id)
        except ValueError:
            pass

    repo = CattleReproductionRepository(db)
    all_cattle = CattleRepository(db).get_all()
    cattle_list = [c for c in all_cattle if c.gender == GenderEnum.FEMALE]
    repro_records = repo.get_all_by_cattle(parsed_cattle_id) if parsed_cattle_id else repo.get_all()

    return templates.TemplateResponse("cattle_reproduction_list.html", {
        "request": request,
        "repro_records": repro_records,
        "cattle_list": cattle_list,
        "selected_cattle_id": parsed_cattle_id,
    })


@router.get("/add-cattle-reproduction/{cattle_id}", response_class=HTMLResponse)
async def add_cattle_reproduction_form(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = CattleRepository(db).get_by_id(cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    all_cattle = CattleRepository(db).get_all()
    male_cattle = [c for c in all_cattle if c.gender == GenderEnum.MALE]
    return templates.TemplateResponse("cattle_reproduction_form.html", {
        "request": request,
        "action": "create",
        "cattle": cattle_data,
        "male_cattle": male_cattle,
    })


@router.get("/edit-cattle-reproduction/{repro_id}", response_class=HTMLResponse)
async def edit_cattle_reproduction_form(request: Request, repro_id: int, db: Session = Depends(get_db)):
    repro = CattleReproductionRepository(db).get_by_id(repro_id)
    if not repro:
        raise HTTPException(status_code=404, detail="Registro reprodutivo não encontrado")
    cattle_data = CattleRepository(db).get_by_id(repro.cattle_id)
    all_cattle = CattleRepository(db).get_all()
    male_cattle = [c for c in all_cattle if c.gender == GenderEnum.MALE]
    return templates.TemplateResponse("cattle_reproduction_form.html", {
        "request": request,
        "action": "edit",
        "cattle": cattle_data,
        "male_cattle": male_cattle,
        "repro": repro,
    })


@router.get("/cattle-timeline/{cattle_id}", response_class=HTMLResponse)
async def cattle_timeline(request: Request, cattle_id: int, db: Session = Depends(get_db)):
    cattle_data = CattleRepository(db).get_by_id(cattle_id)
    if not cattle_data:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    events = CattleReproductionRepository(db).get_timeline_by_cattle(cattle_id)
    return templates.TemplateResponse("cattle_timeline.html", {
        "request": request,
        "cattle": cattle_data,
        "events": events,
    })


@router.get("/health")
def health_check():
    return {"status": "ok"}
