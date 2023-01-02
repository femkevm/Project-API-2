from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Speler(Base):
    __tablename__ = "spelers"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String, index=True)
    achternaam = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    leeftijd = Column(Integer, index=True)
    nationaliteit = Column(String, index=True)
    slaghand = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    enkelspel = relationship("Enkelspel", back_populates="enkel")
    dubbelspel = relationship("Dubbelspel", back_populates="dubbel")


class Enkelspel(Base):
    __tablename__ = "enkelspel"

    id = Column(Integer, primary_key=True, index=True)
    titels = Column(Integer, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    enkelspel_id = Column(Integer, ForeignKey("spelers.id"))

    enkel = relationship("Speler", back_populates="enkelspel")

class Dubbelspel(Base):
    __tablename__ = "dubbelspel"

    id = Column(Integer, primary_key=True, index=True)
    titels = Column(Integer, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    dubbelspel_id = Column(Integer, ForeignKey("spelers.id"))

    dubbel = relationship("Speler", back_populates="dubbelspel")