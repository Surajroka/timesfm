import pandas as pd


def add_ema(
    df: pd.DataFrame,
    short_period: int = 9,
    long_period: int = 21,
) -> pd.DataFrame:
    """Add short and long exponential moving averages."""

    df = df.copy()

    df[f"ema_{short_period}"] = (
        df["close"]
        .ewm(span=short_period, adjust=False)
        .mean()
    )

    df[f"ema_{long_period}"] = (
        df["close"]
        .ewm(span=long_period, adjust=False)
        .mean()
    )

    return df


def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    """Add a simple cumulative VWAP."""

    df = df.copy()

    typical_price = (
        df["high"] +
        df["low"] +
        df["close"]
    ) / 3

    cumulative_price_volume = (
        typical_price * df["volume"]
    ).cumsum()

    cumulative_volume = df["volume"].cumsum()

    df["vwap"] = (
        cumulative_price_volume /
        cumulative_volume.replace(0, float("nan"))
    )

    return df


def add_rsi(
    df: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """Add Relative Strength Index."""

    df = df.copy()

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    average_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    average_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    rs = average_gain / average_loss

    df[f"rsi_{period}"] = 100 - (
        100 / (1 + rs)
    )

    return df


def add_atr(
    df: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """Add Average True Range."""

    df = df.copy()

    previous_close = df["close"].shift(1)

    high_low = df["high"] - df["low"]

    high_close = (
        df["high"] - previous_close
    ).abs()

    low_close = (
        df["low"] - previous_close
    ).abs()

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close,
        ],
        axis=1,
    ).max(axis=1)

    df[f"atr_{period}"] = true_range.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    return df


def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic volume measurements."""

    df = df.copy()

    df["volume_avg_20"] = (
        df["volume"]
        .rolling(20)
        .mean()
    )

    df["relative_volume"] = (
        df["volume"] /
        df["volume_avg_20"]
    )

    return df


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Run the complete technical indicator engine."""

    df = add_ema(df)
    df = add_vwap(df)
    df = add_rsi(df)
    df = add_atr(df)
    df = add_volume_features(df)

    return df