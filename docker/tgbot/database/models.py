from sqlalchemy import BigInteger, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql+asyncpg://postgres:1111@postgres-db/vapecoin'
engine = create_async_engine(DATABASE_URL, echo=False)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id_tg = Column(BigInteger, primary_key=True)
    username_tg = Column(String)
    money = Column(Integer)
    energy = Column(Integer)
    password = Column(String(128))
    image = Column(String)
    moneyhour = Column(Integer)
    
    
class Refferer(Base):
    __tablename__ = 'users_refferer'

    id = Column(Integer, primary_key=True)
    user_id_id = Column(BigInteger, ForeignKey('users.id'))
    ref_link = Column(String)
    ref_user_id_id = Column(Integer, ForeignKey('users.id'))
    

async def async_main():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print('error', e)
