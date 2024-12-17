import pymorphy3
from nltk.corpus import stopwords


morph = pymorphy3.MorphAnalyzer()
stop_words = set(stopwords.words('russian'))


def preprocess_text(text: str) -> str:
    words = text.lower().split()
    lemmas = [
        morph.parse(word)[0].normal_form
        for word in words
    ]
    return ' '.join(lemmas)
