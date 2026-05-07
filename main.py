from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

# Database table create
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="APIVault - API + Database Project")

# Templates folder
templates = Jinja2Templates(directory="templates")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== WEB PAGE ====================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==================== API ENDPOINTS ====================

@app.post("/apis/", response_model=schemas.APIResponse)
def create_api(api: schemas.APICreate, db: Session = Depends(get_db)):
    db_api = models.API(**api.dict())
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api


@app.get("/apis/", response_model=List[schemas.APIResponse])
def get_all_apis(db: Session = Depends(get_db)):
    return db.query(models.API).all()


@app.get("/apis/{api_id}", response_model=schemas.APIResponse)
def get_api(api_id: int, db: Session = Depends(get_db)):
    api = db.query(models.API).filter(models.API.id == api_id).first()
    if api is None:
        raise HTTPException(status_code=404, detail="API not found")
    return api


@app.put("/apis/{api_id}", response_model=schemas.APIResponse)
def update_api(api_id: int, api_update: schemas.APIUpdate, db: Session = Depends(get_db)):
    api = db.query(models.API).filter(models.API.id == api_id).first()
    if api is None:
        raise HTTPException(status_code=404, detail="API not found")
    
    for key, value in api_update.dict(exclude_unset=True).items():
        setattr(api, key, value)
    
    db.commit()
    db.refresh(api)
    return api


@app.delete("/apis/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db)):
    api = db.query(models.API).filter(models.API.id == api_id).first()
    if api is None:
        raise HTTPException(status_code=404, detail="API not found")
    db.delete(api)
    db.commit()
    return {"message": "API deleted successfully"}
