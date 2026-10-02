from pydantic import BaseModel,Field
class RegisterRequest(BaseModel): name:str=Field(min_length=2,max_length=80); email:str=Field(min_length=5,max_length=160); password:str=Field(min_length=8,max_length=128)
class LoginRequest(BaseModel): email:str; password:str
class HomeItem(BaseModel): category:str=Field(min_length=1,max_length=80); quantity:int=Field(ge=1,le=100)
class HomeRequest(BaseModel): budget:float=Field(gt=0,le=10000000); room_type:str; style:str="Modern"; items:list[HomeItem]=Field(min_length=1,max_length=30)
class PartyRequest(BaseModel): budget:float=Field(gt=0,le=10000000); guests:int=Field(ge=1,le=10000); event_type:str; venue:str="Flexible"; city:str="Chennai"; preferences:str=""
class JewelryRequest(BaseModel): budget:float=Field(gt=0,le=10000000); occasion:str; style:str="Elegant"; metal:str="Any"; outfit_description:str=""
