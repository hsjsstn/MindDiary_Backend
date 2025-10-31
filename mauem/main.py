from fastapi import FastAPI
from model.model import FaceAnalyzer, get_available_models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello NKS!"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
