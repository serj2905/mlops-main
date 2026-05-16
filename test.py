import json

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


def test(model_path: str, test_csv: str) -> str:
    """Тестирует модель и сохраняет метрики в model_metrics.json."""
    model = joblib.load(model_path)
    test_df = pd.read_csv(test_csv)

    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    metrics = {
        "accuracy": float(accuracy),
        "report": report,
    }

    metrics_path = "model_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    return metrics_path
