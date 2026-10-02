import hashlib,hmac,secrets
from datetime import datetime,timedelta,timezone
import jwt
from app.config import get_settings

def hash_password(password):
    salt=secrets.token_bytes(16); d=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,210000)
    return f"pbkdf2_sha256$210000${salt.hex()}${d.hex()}"
def verify_password(password,encoded):
    try:
        alg,it,salt,digest=encoded.split("$")
        d=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),int(it))
        return alg=="pbkdf2_sha256" and hmac.compare_digest(d.hex(),digest)
    except Exception:return False
def create_access_token(uid):
    exp=datetime.now(timezone.utc)+timedelta(minutes=get_settings().access_token_expire_minutes)
    return jwt.encode({"sub":str(uid),"exp":exp},get_settings().secret_key,algorithm="HS256")
def decode_access_token(token):
    try:return int(jwt.decode(token,get_settings().secret_key,algorithms=["HS256"])["sub"])
    except Exception:return None
