from data.twelve_data import get_historical_data
from smc.liquidity import detect_liquidity_sweeps


def main():

    print()
    print("SMC LIQUIDITY ENGINE")
    print("=" * 95)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    liquidity = detect_liquidity_sweeps(candles)

    bsl_sweeps = liquidity[
        liquidity["bsl_sweep"]
    ]

    ssl_sweeps = liquidity[
        liquidity["ssl_sweep"]
    ]

    sweeps = liquidity[
        liquidity["bsl_sweep"]
        | liquidity["ssl_sweep"]
    ]

    print()
    print(f"Candles analyzed:     {len(liquidity)}")
    print(f"BSL sweeps:           {len(bsl_sweeps)}")
    print(f"SSL sweeps:           {len(ssl_sweeps)}")
    print(f"Total sweep candles:  {len(sweeps)}")

    print()
    print("LATEST LIQUIDITY SWEEPS")
    print("-" * 95)

    if sweeps.empty:

        print("No liquidity sweeps detected.")

    else:

        display = sweeps[
            [
                "datetime",
                "high",
                "low",
                "close",
                "sweep_direction",
                "sweep_level",
                "sweep_size",
                "bsl_sweep",
                "ssl_sweep",
            ]
        ].tail(15).copy()

        numeric_columns = display.select_dtypes(
            include="number"
        ).columns

        display[numeric_columns] = (
            display[numeric_columns].round(4)
        )

        print(
            display.to_string(index=False)
        )

    latest = liquidity.iloc[-1]

    print()
    print("=" * 95)
    print("CURRENT LIQUIDITY MAP")
    print("=" * 95)

    print(
        f"Current BSL Level: "
        f"${latest['bsl_level']:.2f}"
    )

    print(
        f"Current SSL Level: "
        f"${latest['ssl_level']:.2f}"
    )


if __name__ == "__main__":
    main()