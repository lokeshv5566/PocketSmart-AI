import json
from fastapi import APIRouter,Depends,File,Form,UploadFile,HTTPException
from app.database import save_recommendation,get_history
from app.dependencies import get_current_user
from app.schemas import HomeRequest,PartyRequest,JewelryRequest
from app.services.recommendation_service import generate_home,generate_party,generate_jewelry
router=APIRouter(prefix='/api')
async def save(user,typ,payload,result):
    rid=save_recommendation(user['id'],typ,json.dumps(payload),json.dumps(result)); result['id']=rid; result['planner_type']=typ; return result
@router.post('/generate-home')
async def home(p:HomeRequest,user=Depends(get_current_user)): return await save(user,'home',p.model_dump(),await generate_home(p.model_dump()))
@router.post('/generate-party')
async def party(p:PartyRequest,user=Depends(get_current_user)): return await save(user,'party',p.model_dump(),await generate_party(p.model_dump()))
@router.post('/generate-jewelry')
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form('Elegant'),metal:str=Form('Any'),outfit_description:str=Form(''),outfit_image:UploadFile|None=File(None),user=Depends(get_current_user)):
    p=JewelryRequest(budget=budget,occasion=occasion,style=style,metal=metal,outfit_description=outfit_description); data=None; mime=None
    if outfit_image:
        if not (outfit_image.content_type or '').startswith('image/'): raise HTTPException(400,'Outfit upload must be an image.')
        data=await outfit_image.read()
        if len(data)>5*1024*1024: raise HTTPException(413,'Image must be 5 MB or smaller.')
        mime=outfit_image.content_type
    return await save(user,'jewelry',{**p.model_dump(),'image_attached':bool(data)},await generate_jewelry(p.model_dump(),data,mime))
@router.get('/history')
async def history(user=Depends(get_current_user)):
    return [{'id':x['id'],'planner_type':x['planner_type'],'created_at':x['created_at']} for x in get_history(user['id'])]
