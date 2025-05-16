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
async def total_registrations(year: str = None, programme: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT COUNT(*) as total FROM registrations"
    params = []
    conditions = []
    if year:
        conditions.append("registration_year = %s")
        params.append(year)
    if programme:
        conditions.append("programme = %s")
        params.append(programme)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    cur.execute(query, params)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"total_registrations": result["total"]}

@app.get("/api/registrations-by-programme")
async def registrations_by_programme(year: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT programme, COUNT(*) as count FROM registrations"
    params = []
    if year:
        query += " WHERE registration_year = %s"
        params.append(year)
    query += " GROUP BY programme"
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/registrations-by-school")
async def registrations_by_school(year: str = None, programme: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT school, COUNT(*) as count FROM registrations"
    params = []
    conditions = []
    if year:
        conditions.append("registration_year = %s")
        params.append(year)
    if programme:
        conditions.append("programme = %s")
        params.append(programme)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY school"
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/registrations-by-year")
async def registrations_by_year(programme: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT registration_year, COUNT(*) as count FROM registrations"
    params = []
    if programme:
        query += " WHERE programme = %s"
        params.append(programme)
    query += " GROUP BY registration_year"
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/api/top-schools")
async def top_schools(limit: int = 5, year: str = None, programme: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT school, COUNT(*) as count FROM registrations"
    params = []
    conditions = []
    if year:
        conditions.append("registration_year = %s")
        params.append(year)
    if programme:
        conditions.append("programme = %s")
        params.append(programme)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY school ORDER BY count DESC LIMIT %s"
    params.append(limit)
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
