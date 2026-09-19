from data.twelve_data import get_historical_data
from smc.state import build_smc_state
from strategies.smc_sequence import detect_smc_sequences
from backtesting.engine import backtest_signals


def main():

    print()
    print("SMC STRATEGY BACKTEST")
    print("=" * 100)

    candles = get_historical_data(
        symbol="AAPL",
        interval="5min",
        outputsize=500,
    )

    state = build_smc_state(candles)

    signals = detect_smc_sequences(
        state,
        max_bars=6,
    )

    trades = backtest_signals(
        signals,
        risk_reward=2.0,
        stop_atr_buffer=0.25,
    )

    print()
    print(f"Candles: {len(candles)}")
    print(f"Trades:  {len(trades)}")

    if trades.empty:

        print()
        print("No trades generated.")
        return

    print()
    print("TRADES")
    print("-" * 100)

    display = trades.copy()

    numeric_columns = [
        "entry",
        "stop",
        "target",
        "exit",
        "risk",
        "pnl_per_share",
        "r_multiple",
    ]

    display[numeric_columns] = (
        display[numeric_columns].round(4)
    )

    print(
        display.to_string(index=False)
    )

    wins = trades[
        trades["r_multiple"] > 0
    ]

    losses = trades[
        trades["r_multiple"] < 0
    ]

    win_rate = (
        len(wins) / len(trades)
    ) * 100

    total_r = trades[
        "r_multiple"
    ].sum()

    average_r = trades[
        "r_multiple"
    ].mean()

    print()
    print("=" * 100)
    print("RESULTS")
    print("=" * 100)

    print(f"Total Trades:      {len(trades)}")
    print(f"Winners:           {len(wins)}")
    print(f"Losers:            {len(losses)}")
    print(f"Win Rate:          {win_rate:.2f}%")
    print(f"Total R:           {total_r:.2f}R")
    print(f"Average R/Trade:   {average_r:.2f}R")


if __name__ == "__main__":
    main()