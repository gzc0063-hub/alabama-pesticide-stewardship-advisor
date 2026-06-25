from pathlib import Path

import pandas as pd

from src.disclaimers import HEAP_CITATION


def load_resistance_csv(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path)


def filter_resistance_by_state(frame: pd.DataFrame, state: str) -> pd.DataFrame:
    if "State" not in frame.columns:
        return frame.iloc[0:0].copy()
    return frame[frame["State"].astype(str).str.lower() == state.lower()].copy()


def heap_attribution() -> str:
    return HEAP_CITATION
