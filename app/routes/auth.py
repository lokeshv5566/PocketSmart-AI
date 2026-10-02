from fastapi import APIRouter
from fastapi.responses import JSONResponse,RedirectResponse
from app.auth import create_access_token,hash_password,verify_password
from app.database import create_user,get_user_by_email
from app.schemas import RegisterRequest,LoginRequest
router=APIRouter()
@router.post('/api/register')
async def register(p:RegisterRequest):
    if get_user_by_email(p.email): return JSONResponse({'detail':'Email already registered.'},409)
    uid=create_user(p.email,p.name,hash_password(p.password)); r=JSONResponse({'message':'Registration successful.'}); r.set_cookie('access_token',create_access_token(uid),httponly=True,samesite='lax',max_age=86400); return r
@router.post('/api/login')
async def login(p:LoginRequest):
    u=get_user_by_email(p.email)
    if not u or not verify_password(p.password,u['password_hash']): return JSONResponse({'detail':'Invalid email or password.'},401)
    r=JSONResponse({'message':'Login successful.'}); r.set_cookie('access_token',create_access_token(u['id']),httponly=True,samesite='lax',max_age=86400); return r
@router.post('/logout')
async def logout():
    r=RedirectResponse('/',303); r.delete_cookie('access_token'); return r
