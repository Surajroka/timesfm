import pandas as pd

from indicators.technical import add_atr


def detect_displacement(
    df: pd.DataFrame,
    atr_multiplier: float = 1.0,
    body_ratio_min: float = 0.6,
) -> pd.DataFrame:
    """
    Detect strong directional candles.

    A displacement candle requires:
    - meaningful candle range relative to ATR
    - relatively large real body
    """

    df = add_atr(df)

    df = df.copy()

    candle_range = (
        df["high"] - df["low"]
    )

    candle_body = (
        df["close"] - df["open"]
    ).abs()

    df["body_ratio"] = (
        candle_body /
        candle_range.replace(0, float("nan"))
    )

    df["bullish_displacement"] = (
        (df["close"] > df["open"])
        & (candle_range >= df["atr_14"] * atr_multiplier)
        & (df["body_ratio"] >= body_ratio_min)
    )

    df["bearish_displacement"] = (
        (df["close"] < df["open"])
        & (candle_range >= df["atr_14"] * atr_multiplier)
        & (df["body_ratio"] >= body_ratio_min)
    )

    return df


def detect_fvg(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect basic three-candle Fair Value Gaps.

    Bullish FVG:
        Candle 3 low > Candle 1 high

    Bearish FVG:
        Candle 3 high < Candle 1 low
    """

    df = df.copy()

    df["bullish_fvg"] = False
    df["bearish_fvg"] = False

    df["fvg_top"] = float("nan")
    df["fvg_bottom"] = float("nan")
    df["fvg_size"] = float("nan")

    for i in range(2, len(df)):

        candle_1 = df.iloc[i - 2]
        candle_3 = df.iloc[i]

        # Bullish FVG
        if candle_3["low"] > candle_1["high"]:

            bottom = float(
                candle_1["high"]
            )

            top = float(
                candle_3["low"]
            )

            df.at[
                df.index[i],
                "bullish_fvg",
            ] = True

            df.at[
                df.index[i],
                "fvg_bottom",
            ] = bottom

            df.at[
                df.index[i],
                "fvg_top",
            ] = top

            df.at[
                df.index[i],
                "fvg_size",
            ] = top - bottom

        # Bearish FVG
        elif candle_3["high"] < candle_1["low"]:

            bottom = float(
                candle_3["high"]
            )

            top = float(
                candle_1["low"]
            )

            df.at[
                df.index[i],
                "bearish_fvg",
            ] = True

            df.at[
                df.index[i],
                "fvg_bottom",
            ] = bottom

            df.at[
                df.index[i],
                "fvg_top",
            ] = top

            df.at[
                df.index[i],
                "fvg_size",
            ] = top - bottom

    return df


def build_imbalance_engine(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Run displacement and FVG detection."""

    df = detect_displacement(df)

    df = detect_fvg(df)

    return df