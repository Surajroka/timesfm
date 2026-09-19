import pandas as pd


def backtest_signals(
    df: pd.DataFrame,
    risk_reward: float = 2.0,
    stop_atr_buffer: float = 0.25,
) -> pd.DataFrame:
    """
    Backtest SMC setup signals.

    Rules:
    - Signal is confirmed at candle close.
    - Entry occurs at NEXT candle open.
    - Long stop goes below active swing low.
    - Short stop goes above active swing high.
    - Target uses fixed R multiple.
    - Only one trade at a time.
    """

    trades = []

    i = 0

    while i < len(df) - 1:

        row = df.iloc[i]

        is_long = bool(row["bullish_setup"])
        is_short = bool(row["bearish_setup"])

        if not is_long and not is_short:
            i += 1
            continue

        entry_index = i + 1
        entry_row = df.iloc[entry_index]

        entry_price = float(entry_row["open"])
        atr = float(row["atr_14"])

        if pd.isna(atr):
            i += 1
            continue

        if is_long:

            swing_low = row["active_swing_low"]

            if pd.isna(swing_low):
                i += 1
                continue

            stop_price = (
                float(swing_low)
                - atr * stop_atr_buffer
            )

            risk = entry_price - stop_price

            if risk <= 0:
                i += 1
                continue

            target_price = (
                entry_price
                + risk * risk_reward
            )

            direction = "LONG"

        else:

            swing_high = row["active_swing_high"]

            if pd.isna(swing_high):
                i += 1
                continue

            stop_price = (
                float(swing_high)
                + atr * stop_atr_buffer
            )

            risk = stop_price - entry_price

            if risk <= 0:
                i += 1
                continue

            target_price = (
                entry_price
                - risk * risk_reward
            )

            direction = "SHORT"

        exit_price = None
        exit_index = None
        exit_reason = None

        # Begin checking from the entry candle.
        for j in range(entry_index, len(df)):

            candle = df.iloc[j]

            if direction == "LONG":

                stop_hit = (
                    float(candle["low"])
                    <= stop_price
                )

                target_hit = (
                    float(candle["high"])
                    >= target_price
                )

            else:

                stop_hit = (
                    float(candle["high"])
                    >= stop_price
                )

                target_hit = (
                    float(candle["low"])
                    <= target_price
                )

            # Conservative assumption:
            # if stop and target are both touched
            # in the same candle, count the stop first.
            if stop_hit:

                exit_price = stop_price
                exit_index = j
                exit_reason = "STOP"
                break

            if target_hit:

                exit_price = target_price
                exit_index = j
                exit_reason = "TARGET"
                break

        # If neither was reached before data ends.
        if exit_price is None:

            exit_index = len(df) - 1
            exit_price = float(
                df.iloc[exit_index]["close"]
            )
            exit_reason = "END_OF_DATA"

        if direction == "LONG":

            pnl = exit_price - entry_price

        else:

            pnl = entry_price - exit_price

        r_multiple = pnl / risk

        trades.append(
            {
                "signal_time": row["datetime"],
                "entry_time": entry_row["datetime"],
                "exit_time": df.iloc[exit_index]["datetime"],
                "direction": direction,
                "entry": entry_price,
                "stop": stop_price,
                "target": target_price,
                "exit": exit_price,
                "exit_reason": exit_reason,
                "risk": risk,
                "pnl_per_share": pnl,
                "r_multiple": r_multiple,
            }
        )

        # Don't allow overlapping trades.
        i = exit_index + 1

    return pd.DataFrame(trades)