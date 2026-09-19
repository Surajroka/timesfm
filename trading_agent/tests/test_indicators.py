from data.twelve_data import get_historical_data
from indicators.technical import add_all_indicators


def main():
    print()
    print("INDICATOR ENGINE TEST")
    print("=" * 80)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=100,
    )

    result = add_all_indicators(candles)

    columns = [
        "datetime",
        "close",
        "ema_9",
        "ema_21",
        "vwap",
        "rsi_14",
        "atr_14",
        "relative_volume",
    ]

    display = result[columns].tail(10).copy()

    numeric_columns = display.select_dtypes(
    	 include="number"
    ).columns

    display[numeric_columns] = (
    	display[numeric_columns].round(2)
    )

    print(
    	display.to_string(index=False)
    )

    latest = result.iloc[-1]

    print()
    print("=" * 80)
    print("LATEST AAPL MARKET FEATURES")
    print("=" * 80)

    print(f"Price:           ${latest['close']:.2f}")
    print(f"EMA 9:           ${latest['ema_9']:.2f}")
    print(f"EMA 21:          ${latest['ema_21']:.2f}")
    print(f"VWAP:            ${latest['vwap']:.2f}")
    print(f"RSI 14:           {latest['rsi_14']:.2f}")
    print(f"ATR 14:          ${latest['atr_14']:.2f}")
    print(f"Relative Volume:  {latest['relative_volume']:.2f}x")

    if (
        latest["close"] > latest["ema_9"]
        and latest["ema_9"] > latest["ema_21"]
    ):
        trend = "BULLISH"

    elif (
        latest["close"] < latest["ema_9"]
        and latest["ema_9"] < latest["ema_21"]
    ):
        trend = "BEARISH"

    else:
        trend = "MIXED"

    print()
    print(f"Basic Trend:      {trend}")


if __name__ == "__main__":
    main()