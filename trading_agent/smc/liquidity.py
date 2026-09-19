import pandas as pd

from smc.structure import detect_swings


def detect_liquidity_sweeps(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect basic buy-side and sell-side liquidity sweeps.

    BSL sweep:
        Price trades above a previous confirmed swing high
        but closes back below that level.

    SSL sweep:
        Price trades below a previous confirmed swing low
        but closes back above that level.

    Each active swing level can only be swept once.
    """

    df = detect_swings(df)

    df["bsl_level"] = float("nan")
    df["ssl_level"] = float("nan")

    df["bsl_sweep"] = False
    df["ssl_sweep"] = False

    df["sweep_level"] = float("nan")
    df["sweep_size"] = float("nan")
    df["sweep_direction"] = "NONE"

    active_high = None
    active_low = None

    high_swept = True
    low_swept = True

    for i in range(len(df)):

        row = df.iloc[i]

        # Newly confirmed swings become liquidity levels.
        if row["swing_high"]:
            active_high = float(row["high"])
            high_swept = False

        if row["swing_low"]:
            active_low = float(row["low"])
            low_swept = False

        current_high = float(row["high"])
        current_low = float(row["low"])
        current_close = float(row["close"])

        # Buy-side liquidity sweep:
        # wick above swing high, close back below.
        if (
            active_high is not None
            and not high_swept
            and current_high > active_high
            and current_close < active_high
        ):
            df.at[df.index[i], "bsl_sweep"] = True
            df.at[df.index[i], "sweep_direction"] = "BSL"

            df.at[
                df.index[i],
                "sweep_level",
            ] = active_high

            df.at[
                df.index[i],
                "sweep_size",
            ] = current_high - active_high

            high_swept = True

        # Sell-side liquidity sweep:
        # wick below swing low, close back above.
        if (
            active_low is not None
            and not low_swept
            and current_low < active_low
            and current_close > active_low
        ):
            df.at[df.index[i], "ssl_sweep"] = True

            # In the rare case both sides are swept
            # by one candle, mark it as BOTH.
            if df.at[df.index[i], "sweep_direction"] == "BSL":
                df.at[
                    df.index[i],
                    "sweep_direction",
                ] = "BOTH"
            else:
                df.at[
                    df.index[i],
                    "sweep_direction",
                ] = "SSL"

            df.at[
                df.index[i],
                "sweep_level",
            ] = active_low

            df.at[
                df.index[i],
                "sweep_size",
            ] = active_low - current_low

            low_swept = True

        if active_high is not None:
            df.at[
                df.index[i],
                "bsl_level",
            ] = active_high

        if active_low is not None:
            df.at[
                df.index[i],
                "ssl_level",
            ] = active_low

    return df