"""평가 지표 함수 모음"""
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score,
)


def get_positive_score(pipe, X):
    """모델 파이프라인에서 양성 클래스 확률(또는 결정 점수)을 반환한다."""
    if hasattr(pipe.named_steps["model"], "predict_proba"):
        return pipe.predict_proba(X)[:, 1]
    if hasattr(pipe.named_steps["model"], "decision_function"):
        return pipe.decision_function(X)
    return pipe.predict(X)


def evaluate_all(pipelines: dict, X_test, y_test) -> pd.DataFrame:
    """모든 모델의 성능 지표를 DataFrame으로 반환한다.

    주요 지표: ROC-AUC, PR-AUC, F1 (클래스 불균형 환경 기준)
    """
    results = []
    for name, pipe in pipelines.items():
        y_pred  = pipe.predict(X_test)
        y_score = get_positive_score(pipe, X_test)
        results.append({
            "model":     name,
            "ROC-AUC":   roc_auc_score(y_test, y_score),
            "PR-AUC":    average_precision_score(y_test, y_score),
            "F1":        f1_score(y_test, y_pred, zero_division=0),
            "Precision": precision_score(y_test, y_pred, zero_division=0),
            "Recall":    recall_score(y_test, y_pred, zero_division=0),
            "Accuracy":  accuracy_score(y_test, y_pred),
        })
    return pd.DataFrame(results).sort_values("ROC-AUC", ascending=False)
