from pydantic import BaseModel

class User(BaseModel):
    firstname : str
    lastname : str
    email : str
    phonenumber : int
    age : int

