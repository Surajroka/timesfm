import sqlite3
from pathlib import Path

import pandas as pd


# trading_agent/storage/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"
DATABASE_PATH = STORAGE_DIR / "trading_agent.db"


def get_connection():
    """Create a connection to the local SQLite database."""

    STORAGE_DIR.mkdir(exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the database tables if they do not already exist."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS market_data (
                symbol TEXT NOT NULL,
                datetime TEXT NOT NULL,
                interval TEXT NOT NULL,

                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,

                PRIMARY KEY (symbol, datetime, interval)
            )
            """
        )

        connection.commit()

    print(f"Database ready: {DATABASE_PATH}")


def save_market_data(
    symbol: str,
    interval: str,
    candles: pd.DataFrame,
):
    """Store market candles without creating duplicates."""

    rows_saved = 0

    with get_connection() as connection:

        for _, row in candles.iterrows():

            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO market_data (
                    symbol,
                    datetime,
                    interval,
                    open,
                    high,
                    low,
                    close,
                    volume
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol,
                    str(row["datetime"]),
                    interval,
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row.get("volume", 0)),
                ),
            )

            rows_saved += cursor.rowcount

        connection.commit()

    return rows_saved


def count_market_data():
    """Return number of candles stored."""

    with get_connection() as connection:

        cursor = connection.execute(
            "SELECT COUNT(*) FROM market_data"
        )

        return cursor.fetchone()[0]


if __name__ == "__main__":

    initialize_database()

    total = count_market_data()

    print(f"Stored candles: {total}")