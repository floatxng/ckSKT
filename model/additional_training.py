import pandas as pd
from model.utils import load_pipeline, save_pipeline
from process import preprocess_text


def update_model(data_path="new_data.csv", model_path="model/saved/"):
    pipeline = load_pipeline(model_path)

    df = pd.read_csv(data_path)
    df['processed_text'] = df['text'].apply(preprocess_text)

    pipeline.named_steps['clf'].partial_fit(df['processed_text'], df['label'])

    save_pipeline(pipeline, model_path)
    print("Модель успешно дообучена и сохранена.")


if __name__ == "__main__":
    update_model()
