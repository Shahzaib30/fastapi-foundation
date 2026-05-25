import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def main() -> None:
    data = [
        ("build a react website for my shop", "Web Development"),
        ("create an e-commerce platform using nextjs", "Web Development"),
        ("fix bugs in my python script", "Programming"),
        ("analyze this csv data with pandas", "Data Science"),
        ("train a machine learning model", "AI Solution"),
        ("build an android app for delivery", "Mobile App"),
    ]

    texts = [item[0] for item in data]
    labels = [item[1] for item in data]

    text_clf = Pipeline([
        ("vect", CountVectorizer()),
        ("clf", MultinomialNB()),
    ])

    text_clf.fit(texts, labels)
    joblib.dump(text_clf, "project_classifier.pkl")
    print("Model trained and saved as project_classifier.pkl")


if __name__ == "__main__":
    main()
