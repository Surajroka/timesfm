from data.twelve_data import get_historical_data
from smc.imbalance import build_imbalance_engine


def main():

    print()
    print("SMC DISPLACEMENT / FVG ENGINE")
    print("=" * 100)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    result = build_imbalance_engine(candles)

    bullish_displacement = result[
        result["bullish_displacement"]
    ]

    bearish_displacement = result[
        result["bearish_displacement"]
    ]

    bullish_fvg = result[
        result["bullish_fvg"]
    ]

    bearish_fvg = result[
        result["bearish_fvg"]
    ]

    print()
    print(
        f"Bullish displacement: "
        f"{len(bullish_displacement)}"
    )

    print(
        f"Bearish displacement: "
        f"{len(bearish_displacement)}"
    )

    print(
        f"Bullish FVGs:          "
        f"{len(bullish_fvg)}"
    )

    print(
        f"Bearish FVGs:          "
        f"{len(bearish_fvg)}"
    )

    print()
    print("LATEST FAIR VALUE GAPS")
    print("-" * 100)

    fvgs = result[
        result["bullish_fvg"]
        | result["bearish_fvg"]
    ]

    if fvgs.empty:

        print("No FVGs detected.")

    else:

        display = fvgs[
            [
                "datetime",
                "close",
                "bullish_fvg",
                "bearish_fvg",
                "fvg_bottom",
                "fvg_top",
                "fvg_size",
                "bullish_displacement",
                "bearish_displacement",
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


if __name__ == "__main__":
    main()