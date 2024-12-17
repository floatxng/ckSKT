import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from process import preprocess_text
from sklearn.pipeline import Pipeline

from model.utils import save_pipeline


def visualize_coefficients(vectorizer, model, top_n=20):

    feature_names = np.array(vectorizer.get_feature_names_out())
    coefficients = model.coef_

    sorted_indices = np.argsort(np.abs(coefficients))[-top_n:][::-1]
    top_features = feature_names[sorted_indices]
    top_coefficients = coefficients[sorted_indices]

    plt.figure(figsize=(10, 6))
    plt.barh(top_features, top_coefficients, color='skyblue')
    plt.xlabel("Coefficient Value")
    plt.title("Top Words Influencing Model Predictions (Linear Regression)")
    plt.gca().invert_yaxis()
    plt.show()


def train_model(data_path="saved/data.csv", model_path="saved/"):
    df = pd.read_csv(data_path)
    df['processed_text'] = df['text'].apply(preprocess_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], df['reaction'], test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(min_df=10)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse:.5f}")
    print(f"R-squared: {r2:.5f}")

    visualize_coefficients(vectorizer, model, top_n=20)

    save_pipeline(Pipeline([
        ('tfidf', vectorizer),
        ('regressor', model)
    ]), model_path)
    print(f"Модель сохранена в {model_path}")


if __name__ == "__main__":
    train_model()
