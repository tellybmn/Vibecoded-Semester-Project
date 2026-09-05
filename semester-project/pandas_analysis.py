"""Pandas recreation of the contender-score analysis (Phase 4).

Same contender-score logic as analysis.py/data_loader.py, rebuilt on top
of a pandas DataFrame instead of the hand-rolled TeamRecord objects.
"""

import pandas as pd

TURNOVER_POINT_VALUE = 4
YARDS_PER_POINT = 17
TREND_THRESHOLD = 3
EXPECTED_TEAM_COUNT = 32


def decode_streak(raw_value):
    """Decode Madden's byte-wrapped win/loss streak into a signed length.

    A losing streak of n games is exported as the unsigned byte 256 - n
    (255 -> L1, 254 -> L2, ...); win streaks are plain positive integers.
    """
    return raw_value if raw_value <= 127 else -(256 - raw_value)


def load_standings(path):
    """Read the standings CSV at `path` into a DataFrame with a decoded streak column.

    Preconditions: exactly EXPECTED_TEAM_COUNT rows, `winPct` in [0, 1],
    and `gamesPlayed` nonzero everywhere (it's used as a divisor next).
    """
    df = pd.read_csv(path)

    assert len(df) == EXPECTED_TEAM_COUNT, f"expected {EXPECTED_TEAM_COUNT} teams, found {len(df)}"
    assert df["winPct"].between(0, 1).all(), "winPct out of the valid 0-1 range"
    assert (df["gamesPlayed"] > 0).all(), "gamesPlayed must be greater than 0 for every team"

    df["streakLength"] = df["winLossStreak"].apply(decode_streak)
    return df


def add_contender_score(df):
    """Return a copy of `df` with contender-score, rank, gap, and trend columns added.

    Mirrors analysis.py: turnover margin and yardage margin are each
    normalized per game, combined with the same point-equivalency
    weights, then ranked (tiebreak: turnover differential) and compared
    to the official `rank` column via boolean masking.
    """
    df = df.copy()
    df["turnoverMarginPerGame"] = df["tODiff"] / df["gamesPlayed"]
    df["yardMarginPerGame"] = (df["offTotalYds"] - df["defTotalYds"]) / df["gamesPlayed"]
    df["contenderScore"] = (
        TURNOVER_POINT_VALUE * df["turnoverMarginPerGame"] + df["yardMarginPerGame"] / YARDS_PER_POINT
    )

    df = df.sort_values(["contenderScore", "tODiff"], ascending=False).reset_index(drop=True)
    df["contenderRank"] = df.index + 1
    df["rankGap"] = df["rank"] - df["contenderRank"]
    df["rankGapAbs"] = df["rankGap"].abs()

    df["trend"] = "steady"
    df.loc[df["rankGap"] >= TREND_THRESHOLD, "trend"] = "TRENDING UP"
    df.loc[df["rankGap"] <= -TREND_THRESHOLD, "trend"] = "TRENDING DOWN"
    return df


def top_contenders(df, top_n=8):
    """Return the top `top_n` rows by contender score (df is assumed pre-sorted by it)."""
    return df.head(top_n)


def biggest_rank_gaps(df, count=8):
    """Return the `count` rows with the largest |rankGap|, tiebroken by official rank."""
    return df.sort_values(["rankGapAbs", "rank"], ascending=[False, True]).head(count)
