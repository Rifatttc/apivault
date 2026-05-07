from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="APIVault")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== HOME PAGE ====================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==================== API ROUTES ====================
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


@app.delete("/apis/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db)):
    api = db.query(models.API).filter(models.API.id == api_id).first()
    if api is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(api)
    db.commit()
    return {"message": "Deleted"}
