from data.twelve_data import get_historical_data
from smc.state import build_smc_state


def main():

    print()
    print("UNIFIED SMC STATE ENGINE")
    print("=" * 105)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    state = build_smc_state(candles)

    latest = state.iloc[-1]

    print()
    print("AAPL — CURRENT STATE")
    print("-" * 105)

    print(f"Time:                 {latest['datetime']}")
    print(f"Price:               ${latest['close']:.2f}")

    print()
    print("TECHNICAL")
    print(f"Trend:                {latest['trend']}")
    print(f"EMA Structure:        {latest['ema_structure']}")
    print(f"Price vs VWAP:        {latest['price_vs_vwap']}")
    print(f"Momentum:             {latest['momentum']}")
    print(f"Volume State:         {latest['volume_state']}")
    print(f"ATR %:                {latest['atr_pct_14']:.3f}%")

    print()
    print("STRUCTURE")
    print(f"Structure Trend:      {latest['structure_trend']}")
    print(f"Event Direction:      {latest['event_direction']}")
    print(f"BOS:                  {latest['bos']}")
    print(f"MSS:                  {latest['mss']}")
    print(f"Active Swing High:   ${latest['active_swing_high']:.2f}")
    print(f"Active Swing Low:    ${latest['active_swing_low']:.2f}")

    print()
    print("LIQUIDITY")
    print(f"BSL Sweep:            {latest['bsl_sweep']}")
    print(f"SSL Sweep:            {latest['ssl_sweep']}")
    print(f"Sweep Direction:      {latest['sweep_direction']}")
    print(f"Sweep ATR:            {latest['sweep_atr']:.3f}")

    print()
    print("IMBALANCE")
    print(f"Bullish Displacement: {latest['bullish_displacement']}")
    print(f"Bearish Displacement: {latest['bearish_displacement']}")
    print(f"Bullish FVG:          {latest['bullish_fvg']}")
    print(f"Bearish FVG:          {latest['bearish_fvg']}")

    print()
    print("=" * 105)

    print("RECENT IMPORTANT EVENTS")
    print("-" * 105)

    events = state[
        state["bsl_sweep"]
        | state["ssl_sweep"]
        | state["bos"]
        | state["mss"]
        | state["bullish_fvg"]
        | state["bearish_fvg"]
    ]

    display = events[
        [
            "datetime",
            "close",
            "structure_trend",
            "bos",
            "mss",
            "event_direction",
            "bsl_sweep",
            "ssl_sweep",
            "bullish_displacement",
            "bearish_displacement",
            "bullish_fvg",
            "bearish_fvg",
        ]
    ].tail(20)

    print(
        display.to_string(index=False)
    )


if __name__ == "__main__":
    main()