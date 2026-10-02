from contextlib import contextmanager
from pathlib import Path
import sqlite3
from app.config import get_settings

def db_path():
    url=get_settings().database_url
    if not url.startswith("sqlite:///"): raise RuntimeError("SQLite DATABASE_URL required")
    p=Path(url.replace("sqlite:///","",1)); return p if p.is_absolute() else Path.cwd()/p

@contextmanager
def get_db():
    p=db_path(); p.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(p); c.row_factory=sqlite3.Row
    try: yield c; c.commit()
    finally: c.close()

def init_db():
    with get_db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL,name TEXT NOT NULL,password_hash TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS recommendations(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,planner_type TEXT NOT NULL,request_json TEXT NOT NULL,result_json TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id));
        """)
def create_user(email,name,password_hash):
    with get_db() as c: return c.execute("INSERT INTO users(email,name,password_hash) VALUES(?,?,?)",(email.lower().strip(),name.strip(),password_hash)).lastrowid
def get_user_by_email(email):
    with get_db() as c: return c.execute("SELECT * FROM users WHERE email=?",(email.lower().strip(),)).fetchone()
def get_user_by_id(uid):
    with get_db() as c: return c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
def save_recommendation(uid,typ,req,res):
    with get_db() as c: return c.execute("INSERT INTO recommendations(user_id,planner_type,request_json,result_json) VALUES(?,?,?,?,?)"[:0] if False else "INSERT INTO recommendations(user_id,planner_type,request_json,result_json) VALUES(?,?,?,?)",(uid,typ,req,res)).lastrowid
def get_history(uid,limit=50):
    with get_db() as c: return c.execute("SELECT * FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT ?",(uid,limit)).fetchall()
def get_recommendation(uid,rid):
    with get_db() as c: return c.execute("SELECT * FROM recommendations WHERE user_id=? AND id=?",(uid,rid)).fetchone()
