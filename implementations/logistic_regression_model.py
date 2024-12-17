from abstract.model_interface import AbstractModelInterface
from model.process import preprocess_text
from model.utils import load_pipeline
import os


class LogisticRegressionAbstractModelInterface(AbstractModelInterface):
    def __init__(self, model_path="model/saved/"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена по пути: {model_path}. Запустите train.py для обучения модели.")
        self._pipeline = load_pipeline(model_path)

    def predict(self, news_item_content: str) -> float:
        processed_content = preprocess_text(news_item_content)
        prediction = self._pipeline.predict([processed_content])[0]
        return 0.02 if prediction == 1 else -0.02
