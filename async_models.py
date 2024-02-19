import os

from sqlalchemy import String, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'db_dc')

PG_DNS = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DNS)
Session = async_sessionmaker(bind=engine)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class People(Base):

    __tablename__ = 'async_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    birth_year = Column(String(50), nullable=True)
    eye_color = Column(String(50), nullable=True)
    films = Column(String(300), nullable=True)
    gender = Column(String(50), nullable=True)
    hair_color = Column(String(50), nullable=True)
    height = Column(String(50), nullable=True)
    homeworld = Column(String(300), nullable=True)
    mass = Column(String(50), nullable=True)
    skin_color = Column(String(50), nullable=True)
    species = Column(String(300), nullable=True)
    starships = Column(String(300), nullable=True)
    vehicles = Column(String(300), nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
