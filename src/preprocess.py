"""전처리 함수 모음"""
import numpy as np
import pandas as pd

USE_COLS = {
    "ID": "id",
    "BP16_1": "wkdy_sleep_hours",
    "BP16_2": "wknd_sleep_hours",
    "T_Q_HR": "hear_status",
    "T_Q_HR_1": "hear_device",
    "T_Q_HR_2": "hear_device_freq",
    "T_NQ_OCP": "occ_noise",
    "T_NQ_PH2": "ear_noise",
    "T_NQ_PH2_T": "ear_noise_min",
    "T_Q_VN": "tinnitus",
    "T_Q_VN_1": "tinnitus_6mo",
    "T_Q_VN_2": "tinnitus_dist",
    "LQ4_00": "act_limit",
    "LQ4_13": "hear_act_limit",
    "BP_PHQ_1": "phq_1", "BP_PHQ_2": "phq_2", "BP_PHQ_3": "phq_3",
    "BP_PHQ_4": "phq_4", "BP_PHQ_5": "phq_5", "BP_PHQ_6": "phq_6",
    "BP_PHQ_7": "phq_7", "BP_PHQ_8": "phq_8", "BP_PHQ_9": "phq_9",
    "mh_PHQ_S": "phq_score",
}

MISSING_CODE_MAP = {
    "wkdy_sleep_hours": [88, 99, 888, 999],
    "wknd_sleep_hours": [88, 99, 888, 999],
    "hear_status": [8, 9, 88, 99],
    "hear_device": [8, 9, 88, 99],
    "hear_device_freq": [8, 9, 88, 99],
    "occ_noise": [8, 9, 88, 99],
    "ear_noise": [8, 9, 88, 99],
    "ear_noise_min": [888, 999, 8888, 9999],
    "tinnitus": [8, 9, 88, 99],
    "tinnitus_6mo": [8, 9, 88, 99],
    "tinnitus_dist": [8, 9, 88, 99],
    "act_limit": [8, 9, 88, 99],
    "hear_act_limit": [8, 9, 88, 99],
    **{f"phq_{i}": [8, 9] for i in range(1, 10)},
    "phq_score": [88, 99, 888, 999],
}


def decode_sas_bytes(df: pd.DataFrame) -> pd.DataFrame:
    """SAS 파일에서 bytes로 읽힌 문자열 컬럼을 디코딩한다."""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(
                lambda x: x.decode("cp949", errors="ignore") if isinstance(x, bytes) else x
            )
    return df


def select_rename(df: pd.DataFrame, use_cols: dict) -> pd.DataFrame:
    """사용할 컬럼만 선택하고 영어 컬럼명으로 변환한다."""
    existing = {k: v for k, v in use_cols.items() if k in df.columns}
    return df[list(existing.keys())].rename(columns=existing)


def apply_missing_codes(df: pd.DataFrame, missing_map: dict = None) -> pd.DataFrame:
    """비해당/무응답 코드를 NaN으로 대체한다."""
    if missing_map is None:
        missing_map = MISSING_CODE_MAP
    df = df.copy()
    for col, codes in missing_map.items():
        if col in df.columns:
            df[col] = df[col].replace(codes, np.nan)
    for col in ["wkdy_sleep_hours", "wknd_sleep_hours"]:
        if col in df.columns:
            df.loc[(df[col] < 0) | (df[col] > 24), col] = np.nan
    return df


def make_depression_target(df: pd.DataFrame, threshold: int = 7) -> pd.DataFrame:
    """PHQ-8 총점(phq_3 수면 문항 제외) 기반 우울 위험군 타깃 변수를 생성한다."""
    df = df.copy()
    phq_items = [f"phq_{i}" for i in range(1, 10) if i != 3]
    for col in phq_items:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].where(df[col].between(0, 3), np.nan)
    available = [c for c in phq_items if c in df.columns]
    df["phq8_score"] = df[available].sum(axis=1, skipna=False)
    df["depression_risk"] = np.where(
        df["phq8_score"].isna(), np.nan,
        (df["phq8_score"] >= threshold).astype(int)
    )
    return df


def clip_sleep_hours(df: pd.DataFrame, lower: float = 2, upper: float = 16) -> pd.DataFrame:
    """수면시간 이상치를 물리적 범위로 클리핑한다."""
    df = df.copy()
    for col in ["wkdy_sleep_hours", "wknd_sleep_hours"]:
        if col in df.columns:
            df[col] = df[col].clip(lower=lower, upper=upper)
    return df


def add_missing_indicator(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """결측률이 높은 컬럼에 대해 missing indicator 이진 피처를 생성한다."""
    df = df.copy()
    df[f"{col}_missing"] = df[col].isna().astype(int)
    return df
