from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
import models,schemas
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import requests
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.config import Config
# from google.oauth2 import id_token
# from google.auth.transport import requests

app = FastAPI()

origins = ["http://localhost:3000",]
app.add_middleware(SessionMiddleware,secret_key="idontknow", session_cookie='cookie22')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/student/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/student/auth")
async def auth(request: Request, db: Session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)

        user=db.query(models.Students).filter(models.Students.email==token.get('userinfo')['email']).first()
        if user is None:
            userinfo = token.get('userinfo')
            newUser = models.Students()
            newUser.name = userinfo['name']
            newUser.email = userinfo['email']
            db.add(newUser)
            db.commit()
        loginSession = models.SessionModel()
        loginSession.sessionId = token.get('access_token')
        loginSession.email = token.get('userinfo')['email']
        db.add(loginSession)
        db.commit()
        response = RedirectResponse(url="http://localhost:3000/authredirect/student?token="+str(token.get('access_token')))
        return response
    except ValueError:
        raise HTTPException(status_code=498, detail=ValueError)

@app.get('/student/getuser')
async def auth(request: Request, db: Session=Depends(get_db)):
    token = request.headers["Authorization"]
    userResponse = db.query(models.SessionModel).filter(models.SessionModel.sessionId==token).first()
    email = userResponse.email
    if email:
        userInfo =db.query(models.Students).filter(models.Students.email==email).first()
        response = {
            "user": {
                'name':userInfo.name,
                'email':userInfo.email
            }
        }
        return JSONResponse(status_code=200, content=response) 
    else:
        raise HTTPException(status_code=498, detail={'msg': 'Invalid Token'})

@app.get("/student/get-user-list")
def  read_api(db: Session=Depends(get_db)):
    return db.query(models.Students).all()

@app.get("/student/get-consumption-history")
def get_consumption_history(db: Session=Depends(get_db)):
    return db.query(models.Consumption).all()

@app.post("/student/create-user")
def create_user(user: schemas.Student, db: Session=Depends(get_db)):
    
    user_model = models.Students()
    user_model.name =user.name
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
    mess_menu=requests.get("http://localhost:8001/menu/get-menu-for-day")
    output=mess_menu.json()
    return output



    







