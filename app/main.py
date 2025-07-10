import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.kafka_worker import handle_kafka_messages
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("PLCService lifespan started.")
    init_db()
    kafka_thread = threading.Thread(target=handle_kafka_messages, daemon=True)
    kafka_thread.start()
    yield

app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
