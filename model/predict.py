from model.utils import load_pipeline
from process import preprocess_text
from transformers import pipeline

sentiment_pipeline = pipeline("text-classification", model="blanchefort/rubert-base-cased-sentiment")


def predict_text(text, model_path="saved/"):
    model_pipeline = load_pipeline(model_path)
    processed_text = preprocess_text(text)
    model_prediction = model_pipeline.predict([processed_text])[0]
    sentiment_prediction = sentiment_pipeline(text)

    if sentiment_prediction[0]['label'] == 'NEUTRAL':
        return model_prediction * 0.01

    prediction = model_prediction * 0.01 + sentiment_prediction[0]['score'] * 0.05 * (
        -1 if sentiment_prediction[0]['label'] == 'NEGATIVE' else 1
    )
    return prediction


if __name__ == "__main__":
    text = input("Введите текст новости: ")
    prediction = predict_text(text)
    print(f"Предсказание: {prediction}")
