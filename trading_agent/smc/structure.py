import pandas as pd


def detect_swings(
    df: pd.DataFrame,
    left_bars: int = 3,
    right_bars: int = 3,
) -> pd.DataFrame:
    """Detect confirmed swing highs and swing lows."""

    df = df.copy()

    df["swing_high"] = False
    df["swing_low"] = False

    for i in range(left_bars, len(df) - right_bars):

        current_high = df.iloc[i]["high"]
        current_low = df.iloc[i]["low"]

        left = df.iloc[i - left_bars:i]
        right = df.iloc[i + 1:i + 1 + right_bars]

        is_swing_high = (
            current_high > left["high"].max()
            and current_high > right["high"].max()
        )

        is_swing_low = (
            current_low < left["low"].min()
            and current_low < right["low"].min()
        )

        if is_swing_high:
            df.at[df.index[i], "swing_high"] = True

        if is_swing_low:
            df.at[df.index[i], "swing_low"] = True

    return df


def detect_structure_events(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Track confirmed swing levels and classify structural breaks.

    BOS:
        break in the current structural direction.

    MSS:
        break against the current structural direction.

    Each swing level can trigger only once.
    """

    df = df.copy()

    df["active_swing_high"] = float("nan")
    df["active_swing_low"] = float("nan")

    df["bullish_break"] = False
    df["bearish_break"] = False

    df["bos"] = False
    df["mss"] = False

    df["event_direction"] = "NONE"
    df["structure_trend"] = "NEUTRAL"

    active_high = None
    active_low = None

    high_consumed = True
    low_consumed = True

    structure_trend = "NEUTRAL"

    for i in range(len(df)):

        row = df.iloc[i]

        # A newly confirmed swing becomes the active level.
        if row["swing_high"]:
            active_high = float(row["high"])
            high_consumed = False

        if row["swing_low"]:
            active_low = float(row["low"])
            low_consumed = False

        bullish_break = False
        bearish_break = False

        previous_close = None

        if i > 0:
            previous_close = float(
                df.iloc[i - 1]["close"]
            )

        current_close = float(row["close"])

        # Break above active swing high
        if (
            active_high is not None
            and not high_consumed
            and previous_close is not None
            and previous_close <= active_high
            and current_close > active_high
        ):
            bullish_break = True
            high_consumed = True

        # Break below active swing low
        if (
            active_low is not None
            and not low_consumed
            and previous_close is not None
            and previous_close >= active_low
            and current_close < active_low
        ):
            bearish_break = True
            low_consumed = True

        if bullish_break:

            df.at[df.index[i], "bullish_break"] = True
            df.at[df.index[i], "event_direction"] = "BULLISH"

            if structure_trend == "BEARISH":
                df.at[df.index[i], "mss"] = True
            else:
                df.at[df.index[i], "bos"] = True

            structure_trend = "BULLISH"

        elif bearish_break:

            df.at[df.index[i], "bearish_break"] = True
            df.at[df.index[i], "event_direction"] = "BEARISH"

            if structure_trend == "BULLISH":
                df.at[df.index[i], "mss"] = True
            else:
                df.at[df.index[i], "bos"] = True

            structure_trend = "BEARISH"

        df.at[
            df.index[i],
            "structure_trend",
        ] = structure_trend

        if active_high is not None:
            df.at[
                df.index[i],
                "active_swing_high",
            ] = active_high

        if active_low is not None:
            df.at[
                df.index[i],
                "active_swing_low",
            ] = active_low

    return df


def build_structure(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Run the market-structure engine."""

    df = detect_swings(df)

    df = detect_structure_events(df)

    return df