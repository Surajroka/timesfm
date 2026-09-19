from data.twelve_data import get_historical_data
from smc.structure import build_structure


def main():

    print()
    print("SMC BOS / MSS ENGINE")
    print("=" * 90)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    structure = build_structure(candles)

    swing_highs = structure[
        structure["swing_high"]
    ]

    swing_lows = structure[
        structure["swing_low"]
    ]

    bos_events = structure[
        structure["bos"]
    ]

    mss_events = structure[
        structure["mss"]
    ]

    print()
    print(f"Candles analyzed:       {len(structure)}")
    print(f"Swing highs:            {len(swing_highs)}")
    print(f"Swing lows:             {len(swing_lows)}")
    print(f"BOS events:             {len(bos_events)}")
    print(f"MSS events:             {len(mss_events)}")

    print()
    print("LATEST STRUCTURE EVENTS")
    print("-" * 90)

    events = structure[
        structure["bos"]
        | structure["mss"]
    ]

    if events.empty:

        print("No structure events detected.")

    else:

        print(
            events[
                [
                    "datetime",
                    "close",
                    "event_direction",
                    "bos",
                    "mss",
                    "structure_trend",
                    "active_swing_high",
                    "active_swing_low",
                ]
            ]
            .tail(15)
            .to_string(index=False)
        )

    latest = structure.iloc[-1]

    print()
    print("=" * 90)
    print("CURRENT STRUCTURE")
    print("=" * 90)

    print(
        f"Structure Trend:   "
        f"{latest['structure_trend']}"
    )

    print(
        f"Active Swing High: "
        f"${latest['active_swing_high']:.2f}"
    )

    print(
        f"Active Swing Low:  "
        f"${latest['active_swing_low']:.2f}"
    )


if __name__ == "__main__":
    main()