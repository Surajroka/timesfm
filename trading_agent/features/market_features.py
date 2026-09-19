import pandas as pd

from indicators.technical import add_all_indicators


def classify_trend(row: pd.Series) -> str:
    """Classify basic price/EMA trend structure."""

    if (
        row["close"] > row["ema_9"]
        and row["ema_9"] > row["ema_21"]
    ):
        return "BULLISH"

    if (
        row["close"] < row["ema_9"]
        and row["ema_9"] < row["ema_21"]
    ):
        return "BEARISH"

    return "MIXED"


def classify_vwap(row: pd.Series) -> str:
    """Describe price location relative to VWAP."""

    if row["close"] > row["vwap"]:
        return "ABOVE"

    if row["close"] < row["vwap"]:
        return "BELOW"

    return "AT"


def classify_ema_structure(row: pd.Series) -> str:
    """Describe EMA relationship."""

    if row["ema_9"] > row["ema_21"]:
        return "BULLISH"

    if row["ema_9"] < row["ema_21"]:
        return "BEARISH"

    return "NEUTRAL"


def classify_momentum(row: pd.Series) -> str:
    """Classify momentum using RSI."""

    rsi = row["rsi_14"]

    if pd.isna(rsi):
        return "UNKNOWN"

    if rsi >= 70:
        return "OVERBOUGHT"

    if rsi >= 55:
        return "BULLISH"

    if rsi <= 30:
        return "OVERSOLD"

    if rsi <= 45:
        return "BEARISH"

    return "NEUTRAL"


def classify_volume(row: pd.Series) -> str:
    """Classify relative trading volume."""

    relative_volume = row["relative_volume"]

    if pd.isna(relative_volume):
        return "UNKNOWN"

    if relative_volume >= 3:
        return "EXTREME"

    if relative_volume >= 1.5:
        return "HIGH"

    if relative_volume >= 0.75:
        return "NORMAL"

    return "LOW"


def build_market_features(
    candles: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert raw OHLCV candles into technical indicators
    and standardized market features.
    """

    df = add_all_indicators(candles)

    df["trend"] = df.apply(
        classify_trend,
        axis=1,
    )

    df["price_vs_vwap"] = df.apply(
        classify_vwap,
        axis=1,
    )

    df["ema_structure"] = df.apply(
        classify_ema_structure,
        axis=1,
    )

    df["momentum"] = df.apply(
        classify_momentum,
        axis=1,
    )

    df["volume_state"] = df.apply(
        classify_volume,
        axis=1,
    )

    return df