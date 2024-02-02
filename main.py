from fastapi import FastAPI, Request , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests
from datetime import datetime
import pymongo
from model import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)





# DataBase Connection Settings
client = pymongo.MongoClient('mongodb+srv://kunalsrivastava0301:mongokunal03@cluster0.yveocwk.mongodb.net/')
database = client['userdata']
collection = database['data']


templates = Jinja2Templates(directory="templates")


def random_data():
    url = "https://catfact.ninja/fact" 
    info = requests.get(url)
    data = info.text
    return data




@app.get("/" , response_class=HTMLResponse)
async def index(request : Request):
    data_info = random_data()
    current_date = datetime.now().strftime("%d-%m-%Y")
    return templates.TemplateResponse("home.html" , {"request" : request , "data" : data_info , "date" : current_date})



@app.get("/all-user-details")
async def all_users(requset : Request):
    all_user = database.data.find()
    user = []
    for one_user in all_user:
        user.append(one_user)
    

    return templates.TemplateResponse("userdetail.html" , {"request" : requset , "all_data" : user})



@app.post("/submit")
async def submit_data(request : Request , firstname: str = Form(...), lastname: str = Form(...), email: str = Form(...), phonenumber: int = Form(...), age: int = Form(...)):
    data_info = random_data()
    current_date = datetime.now().strftime("%Y-%m-%d")
    user_data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phonenumber" : phonenumber,
        "age": age
    }

    existing_user = database.data.find_one(user_data)
    
    if existing_user is None:
        database.data.insert_one(user_data)
        return templates.TemplateResponse("home.html" , {"request" : request , "user_data" : user_data,"data" : data_info , "date" : current_date})
    else:
        return templates.TemplateResponse("home.html" , {"request" : request , "user_data" : False, "data" : data_info , "date" : current_date})

        
@app.get("/contact")
async def contact(request : Request):
    return templates.TemplateResponse("contact.html" , {"request" : request})

@app.get("/features")
async def feature(request : Request):
    return templates.TemplateResponse("features.html" , {"request" : request})




