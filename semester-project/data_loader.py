"""Load the weekly standings CSV into TeamRecord objects."""

import csv

from models import TeamRecord

INT_FIELDS = [
    "totalWins", "totalLosses", "totalTies", "gamesPlayed", "tODiff",
    "offTotalYds", "offPassYds", "offRushYds",
    "defTotalYds", "defPassYds", "defRushYds",
    "teamOvr", "capRoom", "capAvailable", "capSpent",
    "rank", "seed", "playoffStatus",
]
FLOAT_FIELDS = ["winPct"]


def decode_streak(raw_value):
    """Decode Madden's byte-wrapped win/loss streak into a signed length.

    The Companion App export represents a losing streak as an unsigned
    byte: a 1-game losing streak comes across as 255, 2 games as 254, and
    so on (256 - n). Win streaks are stored as plain positive integers.
    Returns a positive int for a win streak, negative for a loss streak.
    """
    return raw_value if raw_value <= 127 else -(256 - raw_value)


def _parse_row(row):
    """Convert one raw CSV row (all string values) into a TeamRecord."""
    fields = dict(row)
    for name in INT_FIELDS:
        fields[name] = int(row[name])
    for name in FLOAT_FIELDS:
        fields[name] = float(row[name])

    return TeamRecord(
        team_name=fields["teamName"],
        conference_name=fields["conferenceName"],
        division_name=fields["divisionName"],
        total_wins=fields["totalWins"],
        total_losses=fields["totalLosses"],
        total_ties=fields["totalTies"],
        games_played=fields["gamesPlayed"],
        win_pct=fields["winPct"],
        to_diff=fields["tODiff"],
        off_total_yds=fields["offTotalYds"],
        off_pass_yds=fields["offPassYds"],
        off_rush_yds=fields["offRushYds"],
        def_total_yds=fields["defTotalYds"],
        def_pass_yds=fields["defPassYds"],
        def_rush_yds=fields["defRushYds"],
        team_ovr=fields["teamOvr"],
        cap_room=fields["capRoom"],
        cap_available=fields["capAvailable"],
        cap_spent=fields["capSpent"],
        rank=fields["rank"],
        seed=fields["seed"],
        playoff_status=fields["playoffStatus"],
        streak_length=decode_streak(int(row["winLossStreak"])),
    )


def load_teams(path):
    """Read the standings CSV at `path` and return {team_name: TeamRecord}."""
    teams = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = _parse_row(row)
            teams[record.team_name] = record
    return teams
