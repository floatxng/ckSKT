import joblib


def save_pipeline(pipeline, path: str):
    joblib.dump(pipeline, f"{path}/model.pkl")
    print(f"Модель сохранена в {path}/model.pkl")


def load_pipeline(path: str):
    pipeline = joblib.load(f"{path}/model.pkl")
    print("Модель успешно загружена.")
    return pipeline
