import os

import pandas as pd
import requests
from dotenv import load_dotenv


# Load variables from trading_agent/.env
load_dotenv()

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"


def get_historical_data(
    symbol: str,
    interval: str = "5min",
    outputsize: int = 20,
) -> pd.DataFrame:
    """Download historical candles from Twelve Data."""

    if not API_KEY:
        raise ValueError(
            "Twelve Data API key not found. Check your .env file."
        )

    url = f"{BASE_URL}/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") == "error":
        raise RuntimeError(
            f"Twelve Data error: {data.get('message')}"
        )

    if "values" not in data:
        raise RuntimeError(
            f"Unexpected Twelve Data response: {data}"
        )

    df = pd.DataFrame(data["values"])

    # Convert price/volume columns from text to numbers
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # Convert timestamps
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Twelve Data normally returns newest first.
    # We want oldest -> newest for trading calculations.
    df = (
        df.sort_values("datetime")
        .reset_index(drop=True)
    )

    return df


if __name__ == "__main__":
    print()
    print("ADAPTIVE TRADING AGENT")
    print("=" * 50)

    print("\nConnecting to Twelve Data...")

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=20,
    )

    print("Connection successful.")
    print("\nAAPL - 5 MINUTE CANDLES")
    print("-" * 50)

    print(candles.tail(10).to_string(index=False))

    print("\nRows received:", len(candles))