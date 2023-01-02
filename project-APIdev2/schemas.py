from pydantic import BaseModel


class EnkelspelBase(BaseModel):
    titels: int
    hoogste_positie: int
    huidige_positie: int


class EnkelspelCreate(EnkelspelBase):
    titels: int
    hoogste_positie: int
    huidige_positie: int


class Enkelspel(EnkelspelBase):
    id: int
    enkelspel_id: int

    class Config:
        orm_mode = True

class Dubbelspelbase(BaseModel):
    titels: int
    hoogste_positie: int
    huidige_positie: int

class DubbelspelCreate(EnkelspelBase):
    titels: int
    hoogste_positie: int
    huidige_positie: int


class Dubbelspel(EnkelspelBase):
    id: int
    dubbelspel_id: int

    class Config:
        orm_mode = True

class SpelerBase(BaseModel):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str
    slaghand: str


class SpelerCreate(SpelerBase):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str
    slaghand: str


class Speler(SpelerBase):
    id: int
    is_active: bool
    enkelspel: list[Enkelspel] = []
    dubbelspel: list[Dubbelspel] = []

    class Config:
        orm_mode = True