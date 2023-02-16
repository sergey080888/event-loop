from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_DSN = 'postgresql+asyncpg://user:1234@127.0.0.1:5431/netology'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class SwapiPeople(Base):
    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    birth_year = Column(String(length=10))
    eye_color = Column(String(length=40))
    films = Column(String(length=400))
    gender = Column(String(length=40))
    hair_color = Column(String(length=40))
    height = Column(String(length=40))
    homeworld = Column(String(length=400))
    mass = Column(String(length=40))
    name = Column(String(length=40))
    skin_color = Column(String(length=40))
    species = Column(String(length=400))
    starships = Column(String(length=400))
    vehicles = Column(String(length=400))
