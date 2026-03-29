from transformers import pipeline
from fastapi import HTTPException
from .logger import logger


class SentimentService:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")
        logger.info("SentimentService initialized with HuggingFace pipeline")

    def analyze(self, text: str):
        if not text:
            logger.warning("Empty text received for analysis")
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        logger.info(f"Analyzing text: {text[:50]}...")
        try:
            result = self.classifier(text)
            logger.info(f"Analysis result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")