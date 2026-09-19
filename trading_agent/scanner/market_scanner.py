from config.universe import get_all_symbols
from data.twelve_data import get_historical_data
from database.market_db import (
    count_market_data,
    initialize_database,
    save_market_data,
)


def scan_market(
    interval: str = "5min",
    outputsize: int = 100,
):
    """Download and store recent market data for monitored assets."""

    initialize_database()

    symbols = get_all_symbols()

    print()
    print("ADAPTIVE TRADING AGENT")
    print("=" * 75)
    print(f"Scanning {len(symbols)} assets...")
    print()

    results = {}

    for symbol in symbols:
        try:
            # Download candles from Twelve Data
            candles = get_historical_data(
                symbol=symbol,
                interval=interval,
                outputsize=outputsize,
            )

            # Get the newest candle
            latest = candles.iloc[-1]

            # Keep candles available in memory
            results[symbol] = candles

            # Save candles to our SQLite database
            rows_saved = save_market_data(
                symbol=symbol,
                interval=interval,
                candles=candles,
            )

            print(
                f"{symbol:<8} "
                f"${latest['close']:>10.2f}  "
                f"Volume: {latest.get('volume', 0):>12.0f}  "
                f"Saved: {rows_saved:<3} "
                f"OK"
            )

        except Exception as error:
            print(
                f"{symbol:<8} ERROR: {error}"
            )

    print()
    print("=" * 75)

    print(
        f"Successfully scanned "
        f"{len(results)}/{len(symbols)} assets."
    )

    print(
        f"Total candles in database: "
        f"{count_market_data()}"
    )

    return results


if __name__ == "__main__":
    scan_market()