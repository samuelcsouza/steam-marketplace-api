import importlib

from fastapi import FastAPI

app = FastAPI()

api_module = importlib.import_module("src.routers.api")

app.include_router(api_module.api_router)
