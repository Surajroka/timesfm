import pandas as pd


def detect_smc_sequences(
    state: pd.DataFrame,
    max_bars: int = 6,
) -> pd.DataFrame:
    """
    Detect experimental SMC event sequences.

    Bullish:
        SSL sweep
        -> bullish MSS
        -> bullish FVG

    Bearish:
        BSL sweep
        -> bearish MSS
        -> bearish FVG

    Events must occur in chronological order and within max_bars
    of the initial liquidity sweep.
    """

    df = state.copy()

    df["bullish_setup"] = False
    df["bearish_setup"] = False

    df["setup_direction"] = "NONE"

    df["setup_sweep_index"] = pd.NA
    df["setup_mss_index"] = pd.NA

    bullish_sweep_index = None
    bullish_mss_index = None

    bearish_sweep_index = None
    bearish_mss_index = None

    for i in range(len(df)):

        row = df.iloc[i]

        # --------------------------------
        # Start new potential sequences
        # --------------------------------

        if row["ssl_sweep"]:
            bullish_sweep_index = i
            bullish_mss_index = None

        if row["bsl_sweep"]:
            bearish_sweep_index = i
            bearish_mss_index = None

        # --------------------------------
        # Expire old sequences
        # --------------------------------

        if (
            bullish_sweep_index is not None
            and i - bullish_sweep_index > max_bars
        ):
            bullish_sweep_index = None
            bullish_mss_index = None

        if (
            bearish_sweep_index is not None
            and i - bearish_sweep_index > max_bars
        ):
            bearish_sweep_index = None
            bearish_mss_index = None

        # --------------------------------
        # Bullish MSS after SSL sweep
        # --------------------------------

        if (
            bullish_sweep_index is not None
            and i > bullish_sweep_index
            and row["mss"]
            and row["event_direction"] == "BULLISH"
        ):
            bullish_mss_index = i

        # --------------------------------
        # Bearish MSS after BSL sweep
        # --------------------------------

        if (
            bearish_sweep_index is not None
            and i > bearish_sweep_index
            and row["mss"]
            and row["event_direction"] == "BEARISH"
        ):
            bearish_mss_index = i

        # --------------------------------
        # Bullish FVG after bullish MSS
        # --------------------------------

        if (
            bullish_sweep_index is not None
            and bullish_mss_index is not None
            and i > bullish_mss_index
            and row["bullish_fvg"]
        ):
            df.at[df.index[i], "bullish_setup"] = True
            df.at[df.index[i], "setup_direction"] = "LONG"

            df.at[
                df.index[i],
                "setup_sweep_index",
            ] = bullish_sweep_index

            df.at[
                df.index[i],
                "setup_mss_index",
            ] = bullish_mss_index

            # Consume sequence after signal.
            bullish_sweep_index = None
            bullish_mss_index = None

        # --------------------------------
        # Bearish FVG after bearish MSS
        # --------------------------------

        if (
            bearish_sweep_index is not None
            and bearish_mss_index is not None
            and i > bearish_mss_index
            and row["bearish_fvg"]
        ):
            df.at[df.index[i], "bearish_setup"] = True
            df.at[df.index[i], "setup_direction"] = "SHORT"

            df.at[
                df.index[i],
                "setup_sweep_index",
            ] = bearish_sweep_index

            df.at[
                df.index[i],
                "setup_mss_index",
            ] = bearish_mss_index

            bearish_sweep_index = None
            bearish_mss_index = None

    return df