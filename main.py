from fastapi import FastAPI
from models.schemas import Item
from services.sentiment import SentimentService


app = FastAPI()

sentiment_service = SentimentService()


@app.get("/")
def root() -> dict:
    return {"message": "FastAPI service started"}


@app.get("/predict")
def predict_get(text: str) :
    return sentiment_service.analyze(text)


@app.post("/predict")
def predict_post(item: Item) :
    return sentiment_service.analyze(item.text)
