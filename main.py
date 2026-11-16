from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from pydantic import BaseModel #사용 전에 유용한지 아닌지 여부 확인하는 프로그램
app = FastAPI()

DATABASE_URL = postgresql://postgres.idncnltjwdlhkffcdmnv:nqnCMEkscYd8cyLC@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres

@app.get("/")
def read_home():
    return{
        "hello": "world"
    }
