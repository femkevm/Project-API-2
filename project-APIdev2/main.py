from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth
import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_speler(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/spelers/me", response_model=schemas.Speler)
def read_spelers_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_speler = auth.get_current_active_speler(db, token)
    return current_speler

@app.post("/spelers/", response_model=schemas.Speler)
def maak_speler(speler: schemas.SpelerCreate, db: Session = Depends(get_db)):
    db_speler = crud.get_speler_by_email(db, email=speler.email)
    if db_speler:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.maak_speler(db=db, speler=speler)


@app.get("/spelers/", response_model=list[schemas.Speler])
def lees_spelers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spelers = crud.get_spelers(db, skip=skip, limit=limit)
    return spelers


@app.get("/spelers/{speler_id}", response_model=schemas.Speler)
def lees_speler(speler_id: int, db: Session = Depends(get_db)):
    db_speler = crud.get_speler(db, speler_id=speler_id)
    if db_speler is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return db_speler

@app.put("/spelers/{speler_id}", response_model=schemas.Speler)
def update_speler(speler_id: int, speler: schemas.SpelerCreate, db: Session = Depends(get_db)):
    return crud.update_speler(db=db, speler=speler, speler_id=speler_id)

@app.delete("/spelers/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    crud.verwijder_speler(db=db, speler_id=speler_id)
    return {"message": f"succesvol verwijderd speler met id: {speler_id}"}

@app.post("/spelers/{speler_id}/enkelspel/", response_model=schemas.Enkelspel)
def maak_enkelspel_voor_speler(
    speler_id: int, enkelspel: schemas.EnkelspelCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_enkelspel(db=db, enkelspel=enkelspel, speler_id=speler_id)


@app.get("/enkelspel/", response_model=list[schemas.Enkelspel])
def lees_enkelspel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enkelspel = crud.get_enkelspel(db, skip=skip, limit=limit)
    return enkelspel


@app.delete("/enkelspel/{enkelspel_id}")
def verwijder_enkelspel(enkelspel_id: int, db: Session = Depends(get_db)):
    crud.verwijder_enkelspel(db=db, enkelspel_id=enkelspel_id)
    return {"message": f"succesvol verwijderd enkelspel met id: {enkelspel_id}"}

@app.post("/spelers/{speler_id}/dubbelspel/", response_model=schemas.Dubbelspel)
def maak_dubbelspel_voor_speler(
    speler_id: int, dubbelspel: schemas.DubbelspelCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_dubbelspel(db=db, dubbelspel=dubbelspel, speler_id=speler_id)


@app.get("/dubbelspel/", response_model=list[schemas.Dubbelspel])
def lees_dubbelspel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dubbelspel = crud.get_dubbelspel(db, skip=skip, limit=limit)
    return dubbelspel


@app.delete("/dubbelspel/{dubbelspel_id}")
def verwijder_dubbelspel(dubbelspel_id: int, db: Session = Depends(get_db)):
    crud.verwijder_dubbelspel(db=db, dubbelspel_id=dubbelspel_id)
    return {"message": f"succesvol verwijderd dubbelspel met id: {dubbelspel_id}"}


