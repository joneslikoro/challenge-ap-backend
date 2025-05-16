from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

@app.get("/api/total-registrations")
async def total_registrations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT COUNT(*) as total FROM registrations")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"total_registrations": result["total"]}

@app.get("/api/registrations-by-programme")
async def registrations_by_programme():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT programme, COUNT(*) as count FROM registrations GROUP BY programme")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/registrations-by-school")
async def registrations_by_school():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT school, COUNT(*) as count FROM registrations GROUP BY school")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/registrations-by-year")
async def registrations_by_year():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT registration_year, COUNT(*) as count FROM registrations GROUP BY registration_year")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/top-schools")
async def top_schools(limit: int = 5):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT school, COUNT(*) as count FROM registrations GROUP BY school ORDER BY count DESC LIMIT %s", (limit,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
