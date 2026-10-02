import json
from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import get_history,get_recommendation
from app.dependencies import current_user_from_token
router=APIRouter(); t=Jinja2Templates(directory='templates')
def u(r): return current_user_from_token(r.cookies.get('access_token'))
@router.get('/',response_class=HTMLResponse)
async def index(r:Request): return t.TemplateResponse('index.html',{'request':r,'user':u(r)})
@router.get('/login',response_class=HTMLResponse)
async def login(r:Request): return t.TemplateResponse('login.html',{'request':r,'user':u(r)})
@router.get('/register',response_class=HTMLResponse)
async def register(r:Request): return t.TemplateResponse('register.html',{'request':r,'user':u(r)})
@router.get('/dashboard',response_class=HTMLResponse)
async def dashboard(r:Request):
    user=u(r)
    if not user:return RedirectResponse('/login',303)
    return t.TemplateResponse('dashboard.html',{'request':r,'user':user,'history':get_history(user['id'],6)})
@router.get('/history',response_class=HTMLResponse)
async def history(r:Request):
    user=u(r)
    if not user:return RedirectResponse('/login',303)
    rows=[]
    for x in get_history(user['id']):
        d=dict(x);d['result']=json.loads(d['result_json']);rows.append(d)
    return t.TemplateResponse('history.html',{'request':r,'user':user,'records':rows})
@router.get('/planner/{typ}',response_class=HTMLResponse)
async def planner(r:Request,typ:str):
    if not u(r):return RedirectResponse('/login',303)
    return t.TemplateResponse('planner.html',{'request':r,'user':u(r),'planner_type':typ}) if typ in {'home','party','jewelry'} else RedirectResponse('/dashboard',303)
@router.get('/recommendations/{rid}',response_class=HTMLResponse)
async def detail(r:Request,rid:int):
    user=u(r)
    if not user:return RedirectResponse('/login',303)
    row=get_recommendation(user['id'],rid)
    if not row:return RedirectResponse('/history',303)
    return t.TemplateResponse('recommendations.html',{'request':r,'user':user,'record':row,'result':json.loads(row['result_json'])})
