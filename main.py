import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import cattle, cattle_weight, web
from app.routers import cattle

# Create database tables if they don't exist (Alembic is preferred for production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Auditoria de Rebanho")

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(cattle.router)
app.include_router(cattle_weight.router)
app.include_router(web.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8008, reload=True)
