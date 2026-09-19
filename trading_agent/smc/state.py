import pandas as pd

from features.market_features import build_market_features
from smc.structure import build_structure
from smc.liquidity import detect_liquidity_sweeps
from smc.imbalance import build_imbalance_engine


def build_smc_state(
    candles: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build one unified technical + SMC state table.

    Each row represents information available for that candle.
    """

    # Technical features
    technical = build_market_features(candles)

    # Structure
    structure = build_structure(candles)

    # Liquidity
    liquidity = detect_liquidity_sweeps(candles)

    # Displacement / FVG
    imbalance = build_imbalance_engine(candles)

    state = technical.copy()

    # -------------------------
    # STRUCTURE
    # -------------------------

    structure_columns = [
        "swing_high",
        "swing_low",
        "active_swing_high",
        "active_swing_low",
        "bullish_break",
        "bearish_break",
        "bos",
        "mss",
        "event_direction",
        "structure_trend",
    ]

    for column in structure_columns:
        state[column] = structure[column]

    # -------------------------
    # LIQUIDITY
    # -------------------------

    liquidity_columns = [
        "bsl_level",
        "ssl_level",
        "bsl_sweep",
        "ssl_sweep",
        "sweep_level",
        "sweep_size",
        "sweep_direction",
    ]

    for column in liquidity_columns:
        state[column] = liquidity[column]

    # -------------------------
    # IMBALANCE
    # -------------------------

    imbalance_columns = [
        "body_ratio",
        "bullish_displacement",
        "bearish_displacement",
        "bullish_fvg",
        "bearish_fvg",
        "fvg_bottom",
        "fvg_top",
        "fvg_size",
    ]

    for column in imbalance_columns:
        state[column] = imbalance[column]

    # -------------------------
    # NORMALIZED MEASUREMENTS
    # -------------------------

    state["sweep_atr"] = (
        state["sweep_size"] /
        state["atr_14"]
    )

    state["fvg_atr"] = (
        state["fvg_size"] /
        state["atr_14"]
    )

    candle_range = (
        state["high"] -
        state["low"]
    )

    state["range_atr"] = (
        candle_range /
        state["atr_14"]
    )

    return state