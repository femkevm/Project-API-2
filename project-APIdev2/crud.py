from sqlalchemy.orm import Session

import models
import schemas
import auth


def get_speler(db: Session, speler_id: int):
    return db.query(models.Speler).filter(models.Speler.id == speler_id).first()


def get_speler_by_email(db: Session, email: str):
    return db.query(models.Speler).filter(models.Speler.email == email).first()


def get_spelers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Speler).offset(skip).limit(limit).all()


def maak_speler(db: Session, speler: schemas.SpelerCreate):
    hashed_password = auth.get_password_hash(speler.hashed_password)
    db_speler = models.Speler(naam=speler.naam, achternaam=speler.achternaam, email=speler.email, hashed_password=hashed_password,leeftijd=speler.leeftijd, nationaliteit=speler.nationaliteit, slaghand=speler.slaghand)
    db.add(db_speler)
    db.commit()
    db.refresh(db_speler)
    return db_speler

def update_speler(db: Session, speler: schemas.SpelerCreate, speler_id: int):
    db_speler = get_speler(db=db, speler_id=speler_id)
    db_speler.naam = speler.naam
    db_speler.achternaam = speler.achternaam
    db_speler.email= speler.email
    db_speler.hashed_password= speler.hashed_password
    db_speler.leeftijd = speler.leeftijd
    db_speler.nationaliteit = speler.nationaliteit
    db_speler.slaghand = speler.slaghand
    db.commit()
    db.refresh(db_speler)
    return db_speler


def verwijder_speler(db: Session,speler_id: int):
    db.query(models.Speler).filter(models.Speler.id== speler_id).delete()
    db.commit()

def get_enkelspel(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Enkelspel).offset(skip).limit(limit).all()


def maak_speler_enkelspel(db: Session, enkelspel: schemas.EnkelspelCreate, speler_id: int):
    db_enkelspel = models.Enkelspel(**enkelspel.dict(), enkelspel_id=speler_id)
    db.add(db_enkelspel)
    db.commit()
    db.refresh(db_enkelspel)
    return db_enkelspel


def verwijder_enkelspel(db: Session,enkelspel_id: int):
    db.query(models.Enkelspel).filter(models.Enkelspel.id== enkelspel_id).delete()
    db.commit()

def get_dubbelspel(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dubbelspel).offset(skip).limit(limit).all()


def maak_speler_dubbelspel(db: Session, dubbelspel: schemas.DubbelspelCreate, speler_id: int):
    db_dubbelspel = models.Dubbelspel(**dubbelspel.dict(), dubbelspel_id=speler_id)
    db.add(db_dubbelspel)
    db.commit()
    db.refresh(db_dubbelspel)
    return db_dubbelspel


def verwijder_dubbelspel(db: Session,dubbelspel_id: int):
    db.query(models.Dubbelspel).filter(models.Dubbelspel.id== dubbelspel_id).delete()
    db.commit()

def create_user(db: Session, speler: schemas.SpelerCreate):
    hashed_password = auth.get_password_hash(speler.password)
    db_user = models.Speler(email=speler.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user