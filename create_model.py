import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import spacy


"""
This function takes a list of texts, and breaks them down with spacy to be used by the machine
learning algorithms. 
"""
def extract_features(texts, nlp):
    features = []
    for doc in nlp.pipe(texts, disable=["parser", "ner"]):
        doc_features = []
        for token in doc:
            doc_features.extend([token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                                 token.shape_])
        features.append(doc_features)
    return features


def create_korean_model():
    print("GETTING SPACY MODELS")
    if not spacy.util.is_package("ko_core_news_sm"):
        spacy.cli.download("ko_core_news_sm")
    korean_nlp = spacy.load('ko_core_news_sm')

    print("GETTING TRAINING DATA")
    df = pd.read_csv('korean/sentences.csv')
    X_train, X_test, y_train, y_test = train_test_split(df['sentence'], df['level'], test_size=0.2, random_state=42)

    print("EXTRACTING FEATURES")
    X_train_features = extract_features(X_train, korean_nlp)
    X_test_features = extract_features(X_test, korean_nlp)

    print("VECTORIZING")
    vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=2)
    X_train_tfidf = vectorizer.fit_transform(X_train_features)
    X_test_tfidf = vectorizer.transform(X_test_features)

    print("TRAINING MODELS")
    model = LogisticRegression(random_state=42)
    model.fit(X_train_tfidf, y_train)

    print("PREDICTING USING DATA")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Accuracy: {accuracy * 100:.2f}%')

create_korean_model()
