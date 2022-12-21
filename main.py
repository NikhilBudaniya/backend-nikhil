from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
import models,schemas
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import requests

from google.oauth2 import id_token
from google.auth.transport import requests

app = FastAPI()

origins = ["http://localhost:3000",]
app.add_middleware(SessionMiddleware,secret_key="idontknow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/student/auth")
def authentication(request:Request,token:str):
    try:
        user = id_token.verify_oauth2_token(token,requests.Request(),"755763254755-6ocup3m4qshnhn3of7cgvf74f16hp3qg.apps.googleusercontent.com")

        request.session['user']=dict({
            "email": user["email"]
        })
        return user['name']+'Logged In successfully'
    except ValueError:
        return "unauthorized"

@app.get("/student/get-user-list")
def  read_api(db: Session=Depends(get_db)):
    return db.query(models.Students).all()

@app.get("/student/get-consumption-history")
def get_consumption_history(db: Session=Depends(get_db)):
    return db.query(models.Consumption).all()

@app.post("/student/create-user")
def create_user(user: schemas.Student, db: Session=Depends(get_db)):
    
    user_model = models.Students()
    user_model.first_name = user.first_name
    user_model.last_name =user.last_name
    user_model.password = user.password
    user_model.Age = user.Age
    user_model.Gender= user.Gender
    user_model.Address_line_1=user.Address_line_1
    user_model.Address_line_2=user.Address_line_2
    user_model.City=user.City
    user_model.State=user.State
    user_model.Pincode=user.Pincode
    user_model.Country=user.Country
    user_model.Phone=user.Phone
    user_model.email=user.email


    db.add(user_model)
    db.commit()

    return user

@app.post("/student/add-consumption-history")
def add_consumption_history(foodconsumption:schemas.FoodConsumption, db: Session=Depends(get_db)):

    consumption_model = models.Consumption()
    consumption_model.student_phone=foodconsumption.student_phone
    consumption_model.date=foodconsumption.date
    consumption_model.type=foodconsumption.type
    consumption_model.total_calories=foodconsumption.total_calories

    db.add(consumption_model)
    db.commit()

    return foodconsumption



@app.put("/student/update-user/{user_id}")
def update_user(user_id:int, user:schemas.Student,db:Session=Depends(get_db)):
    user_model=db.query(models.Students).filter(models.Users.id==user_id).first()

    if user_model is None:
        raise  HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does Not Exist"
        )

    user_model.first_name = user.first_name
    user_model.last_name =user.last_name
    user_model.password = user.password
    user_model.Age = user.Age
    user_model.Gender= user.Gender
    user_model.Address_line_1=user.Address_line_1
    user_model.Address_line_2=user.Address_line_2
    user_model.City=user.City
    user_model.State=user.State
    user_model.Pincode=user.Pincode
    user_model.Country=user.Country
    user_model.Phone=user.Phone
    user_model.email=user.email
    user_model.DOB=user.DOB

    db.add(user_model)
    db.commit()

    return user

@app.post("/student/isNewUser/{email_id}")
def isNewUser(email_id, user:schemas.Student,db:Session=Depends(get_db)):

    user_model=user_model=db.query(models.Students).filter(models.Users.email==email_id).first()

    if user_model:
        return True
    return False

@app.get("/student/get-mess_menu")
def get_mess_menu():
    mess_menu=requests.get("http://localhost:8001/vendor/mess_menu")
    return mess_menu



    







