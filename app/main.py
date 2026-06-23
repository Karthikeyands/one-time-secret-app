# app/main.py
import os
import time
import psycopg2
from psycopg2 import OperationalError
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .db import engine, Base

# -------------------------------------------------
# ❶  Detect test mode
IS_TEST = os.getenv("TESTING") == "1"
# -------------------------------------------------

def wait_for_postgres(dsn: str):
    while True:
        try:
            conn = psycopg2.connect(dsn)
            conn.close()
            print("✅ PostgreSQL is available.")
            break
        except OperationalError:
            print("⏳ Waiting for PostgreSQL...")
            time.sleep(1)

# -------------------------------------------------
# ❷  Only run these lines when NOT testing
if not IS_TEST:
    wait_for_postgres(dsn=os.environ["POS_SQL"])
    Base.metadata.create_all(bind=engine)
# -------------------------------------------------

def create_app() -> FastAPI:
    from .routes import router
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(router)
    return app

app = create_app()

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

@app.get("/secret/{secret_id}")
def secret_page(secret_id: str):
    return FileResponse("app/static/secret.html")
