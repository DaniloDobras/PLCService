import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.kafka_worker import start_kafka_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("PLCService lifespan started.")
    kafka_thread = threading.Thread(target=start_kafka_consumer, daemon=True)
    kafka_thread.start()
    yield

app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
