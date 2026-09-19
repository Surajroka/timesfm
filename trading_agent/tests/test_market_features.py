from data.twelve_data import get_historical_data
from features.market_features import build_market_features


def main():

    print()
    print("MARKET FEATURE ENGINE")
    print("=" * 65)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=100,
    )

    features = build_market_features(candles)

    latest = features.iloc[-1]

    print()
    print("AAPL - LATEST MARKET STATE")
    print("-" * 65)

    print(f"Price:              ${latest['close']:.2f}")
    print(f"EMA 9:              ${latest['ema_9']:.2f}")
    print(f"EMA 21:             ${latest['ema_21']:.2f}")
    print(f"Session VWAP:       ${latest['vwap']:.2f}")

    print()
    print(f"Trend:               {latest['trend']}")
    print(f"EMA Structure:       {latest['ema_structure']}")
    print(f"Price vs VWAP:       {latest['price_vs_vwap']}")
    print(f"Momentum:            {latest['momentum']}")

    print()
    print(f"RSI 14:              {latest['rsi_14']:.2f}")
    print(f"ATR 14:             ${latest['atr_14']:.2f}")
    print(f"ATR %:               {latest['atr_pct_14']:.3f}%")
    print(f"Relative Volume:     {latest['relative_volume']:.2f}x")
    print(f"Volume State:        {latest['volume_state']}")

    print()
    print("=" * 65)


if __name__ == "__main__":
    main()