import os
os.environ['DATABASE_URL']='sqlite:///./test_pocketsmart.db';os.environ['SECRET_KEY']='test-secret'
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
@pytest.fixture
def client():
 p=Path('test_pocketsmart.db')
 if p.exists():p.unlink()
 init_db()
 with TestClient(app) as c:yield c
 if p.exists():p.unlink()
