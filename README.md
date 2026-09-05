# RYZE CFM Contender Analysis — Semester Project

A front-office analyst tool for a real, in-progress Madden 27 franchise league.
Six weeks into the season, this project separates teams that are winning because
of the underlying numbers from teams riding a record their box score doesn't
support.

## Dataset

`semester-project/phase0_dataset/ryze_cfm_madden27_2026_week6_standings.csv` —
32 teams, 22 columns, pulled from the league's Madden Companion App standings
export right after week 6 finished. Every stat is the game's own running
total since week 1 (not averaged or estimated). `ptsFor`/`ptsAgainst` were
dropped from the original export because they're known to be broken in EA's
Companion App output.

## Goal

For each team, compute a custom **contender score** from turnover
differential and total-yardage differential (each normalized per game so
bye-week teams aren't penalized), rank all 32 teams by that score, and compare
the result to the game's own official `rank` column. Teams whose contender
score ranks much better than their official rank are flagged **trending up**
(their record hasn't caught up to their underlying numbers yet); teams whose
official rank is much better than their contender score are flagged
**trending down** (a hot record without the numbers to back it up).

The official `rank`, `seed`, and `playoffStatus` columns are never used as
inputs to the score — only as the thing the score is checked against.

## Running it

```
python3 semester-project/main.py
```

Prints a ranked leaderboard of the top 8 projected true contenders and the
biggest gaps between the contender-score ranking and the official standings,
and saves the same report to `semester-project/week6_contender_report.txt`.

A pandas/matplotlib version of the same analysis (Phase 4) is available too:

```
pip install -r requirements.txt
python3 semester-project/main_pandas.py
```

This reloads the CSV into a `DataFrame`, recreates the contender score and
trending flags with vectorized DataFrame operations, saves the ranked
report as `semester-project/week6_contender_report_pandas.csv`, and saves
two charts built with `.plot()`:
`semester-project/top_contenders_chart.png` (bar chart of the top 8
contender scores) and `semester-project/yardage_vs_turnovers_chart.png`
(yardage margin vs. turnover differential, colored by playoff status).

## Project history

This project was built in phases matching the semester's module progression:

- **Phase 0 / 1** — dataset + a single hand-rolled script (`csv` module, dict
  of dicts, no dataframe libraries).
- **Phase 2** — refactored into modules (`data_loader.py`, `models.py`,
  `analysis.py`, `report.py`) with docstrings and a `TeamRecord` data class.
- **Phase 3** — multi-key custom sorting and precondition checks.
- **Phase 4** — a pandas/matplotlib version alongside the original, producing
  saved chart PNGs.
