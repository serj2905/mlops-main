import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression


def train(train_csv: str) -> str:
    """Обучает модель логистической регрессии и сохраняет ее в model.pkl."""
    train_df = pd.read_csv(train_csv)

    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    model_path = "model.pkl"
    joblib.dump(model, model_path)

    return model_path
