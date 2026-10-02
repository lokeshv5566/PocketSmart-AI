from fastapi import Cookie,HTTPException,Request
from app.auth import decode_access_token
from app.database import get_user_by_id

def current_user_from_token(token):
    uid=decode_access_token(token) if token else None
    return get_user_by_id(uid) if uid else None
def get_current_user(request:Request,access_token:str|None=Cookie(default=None)):
    u=current_user_from_token(access_token)
    if not u: raise HTTPException(401,"Authentication required.")
    return u
