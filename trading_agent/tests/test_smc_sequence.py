from data.twelve_data import get_historical_data
from smc.state import build_smc_state
from strategies.smc_sequence import detect_smc_sequences


def main():

    print()
    print("SMC SEQUENCE DETECTOR")
    print("=" * 100)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    state = build_smc_state(candles)

    result = detect_smc_sequences(
        state,
        max_bars=6,
    )

    setups = result[
        result["bullish_setup"]
        | result["bearish_setup"]
    ]

    print()
    print(f"Candles analyzed: {len(result)}")
    print(f"Setups detected:  {len(setups)}")

    print()
    print("DETECTED SETUPS")
    print("-" * 100)

    if setups.empty:

        print("No complete sequences detected.")

    else:

        print(
            setups[
                [
                    "datetime",
                    "close",
                    "setup_direction",
                    "structure_trend",
                    "price_vs_vwap",
                    "ema_structure",
                    "momentum",
                    "relative_volume",
                    "setup_sweep_index",
                    "setup_mss_index",
                ]
            ]
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()