"""피처 엔지니어링 함수 모음"""
import pandas as pd


def add_sleep_features(df: pd.DataFrame) -> pd.DataFrame:
    """수면 관련 파생 피처를 추가한다.

    - sleep_short : 주중 수면 6시간 미만 이진 지시자
    - sleep_diff  : 주말 수면 − 주중 수면 (수면 패턴 변화)
    """
    df = df.copy()
    if "wkdy_sleep_hours" in df.columns:
        df["sleep_short"] = (df["wkdy_sleep_hours"] < 6).astype(int)
    if "wkdy_sleep_hours" in df.columns and "wknd_sleep_hours" in df.columns:
        df["sleep_diff"] = df["wknd_sleep_hours"] - df["wkdy_sleep_hours"]
    return df


FEATURE_COLS = [
    "wkdy_sleep_hours",
    "wknd_sleep_hours",
    "hear_status",
    "hear_device",
    "hear_device_freq",
    "occ_noise",
    "ear_noise",
    "ear_noise_min",
    "tinnitus",
    "tinnitus_6mo",
    "tinnitus_dist",
    "act_limit",
    "hear_act_limit",
    # 파생 피처
    "hear_device_freq_missing",
    "sleep_short",
    "sleep_diff",
]

NUMERIC_FEATURES = [
    "wkdy_sleep_hours",
    "wknd_sleep_hours",
    "ear_noise_min",
    "tinnitus_dist",
    "sleep_diff",
    "sleep_short",
    "hear_device_freq_missing",
]
