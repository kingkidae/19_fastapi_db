# sql 언어를 이용하지 않고, ORM을 이용해서 자바스크립트에서는 자바스크립트 언어로, 파이썬에서는 파이썬 언어로 SQL을 다루게 해주는 것이 sqlalchemy임.
# 터미널에 
# uv add sqlalchemy
# uv add psycopg
# uv add psycopg2-binary
# 설치

from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy import create_engine, Column, Integer, String # sqlalchemy는 db를 다루는 라이브러리로 유효성을 검사함.
from sqlalchemy.orm import declarative_base, Session
from pydantic import BaseModel #사용 전에 유용한지 아닌지 여부 확인하는 라이브러리
app = FastAPI()

DATABASE_URL = "postgresql://postgres.idncnltjwdlhkffcdmnv:nqnCMEkscYd8cyLC@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"
# 슈파베이스 프로젝트 오버뷰 해서 커넥트 누르고, 다이렉트 커넥트, 세션풀러 선택해서 스크롤 내리면 커넥트 스트링 옆에 쉐어드풀러 에 있는 링크입력하면 됨. 링크 내 [유어 패스워드]비번은 프로젝트 생성할 때 정한 비번치면 됨. 대괄호까지 없애줘야 함.
# 비번 까먹었을 때 슈파베이스 - 데이터베이스 - 세팅즈 - 리셋 패스워드눌리면 재설정 가능함. DB같은 경우는 평소쓰던 비번 쓰면 리스키하기 때문에 비번 재생성 만드는 창에서 제너레이트 패스워드하면 어려운 비번 알아서 세팅해줌.
engine = create_engine(DATABASE_URL)
Base = declarative_base()

#table model 생성 (table name: users) 클래스는 객체를 만들어주는 명령어임.
class User(Base): #테이블을 정의함. 슈파베이스 들어가보면 users라는 테이블이 있음.
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, index = True)
    email = Column(String(120))
class UserCreate(BaseModel):
    username : str
    email : str

#테이블 없을 때 생성해주는 함수
Base.metadata.create_all(bind=engine)

#요청 받아 세션을 열고 끝나면 닫는 함수
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


# primary_key 적으면 자동으로 인덱스 설정됨.
# index = true 를 적어주면 빠르게 찾아주는 것임.

#포스트 요청 (=회원가입) CRUD 중 Create
@app.post("/users")
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    new_user = User(username = user.username, email = user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "ok": "true",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
#프론트에서 user.username하고 user.email을 받으면 username과email을 가진 nrw_user라는 객체가 생김

# 가입한 정보 불러오기(전체 조회) CRUD 중 Read
@app.get("/users")
def read_users(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return[
        {"id": user.id, 
         "username":user.username, 
         "email":user.email
        } for user in users
    ]
#/users 경로로 가면 가입, 조회가 됨.

# 가입한 정보 불러오기(특정 조회) CRUD 중 Read
@app.get("/users/{user_id}")
def read_user(user_id:int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="there is no such name.")
    # 유저가 없는 경우에 사용자가 없다는 데이터를 보내줌. 반드시 들어가야 함.
    return {
        "id": user.id,
        "username" : user.username,
        "email" : user.email,
    }
    #퍼스트는 찾은 것 중에 가장 첫번째꺼 인덱스 0번을 가져와라 이뜻임.

# 회원정보 업데이트하기  CRUD 중 Update
@app.put("/users/{user_id}")
def update_user(user_id:int, data:UserCreate, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="there is no such name.")

    user.username = data.username
    user.email = data.email
    db.commit() #db를 확정하는 코드
    db.refresh(user)
    return{
        "id" : user.id,
        "username": user.username,
        "email" : user.email,
    }


# 회원정보 삭제 CRUD 중 Delete
@app.delete("/users/{user_id}")
def delete_user(user_id:int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # db에서 하나의 행을 가져와서 user라는 객체로 만들어줌.
    if user is None:
        return HTTPException(status_code=404, detail="there's no such name.")
    db.delete(user)
    db.commit()
    return {"message": "delete completed."}



@app.get("/")
def read_home():
    return{
        "hello": "world"
    }
# 그냥 / 이 경로로 가면 헬로월드 나옴.