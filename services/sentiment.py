from transformers import pipeline
from fastapi import HTTPException


class SentimentService:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")

    def analyze(self, text: str):
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        return self.classifier(text)