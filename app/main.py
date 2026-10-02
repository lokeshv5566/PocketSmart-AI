from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import init_db
from app.routes import pages,auth,planners
@asynccontextmanager
async def lifespan(app): init_db(); yield
s=get_settings(); app=FastAPI(title=s.app_name,version='1.0.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:8000','http://127.0.0.1:8000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
Path('static').mkdir(exist_ok=True); app.mount('/static',StaticFiles(directory='static'),name='static')
app.include_router(pages.router);app.include_router(auth.router);app.include_router(planners.router)
@app.get('/health')
async def health():return {'status':'ok','app':s.app_name}
