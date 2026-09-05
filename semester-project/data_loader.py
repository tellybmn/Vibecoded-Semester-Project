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
REQUIRED_COLUMNS = frozenset(INT_FIELDS) | frozenset(FLOAT_FIELDS) | {
    "teamName", "conferenceName", "divisionName", "winLossStreak",
}
EXPECTED_TEAM_COUNT = 32


def _parse_number(raw_value, field_name, team_name, cast):
    """Cast a raw CSV string to `cast` (int or float), erroring with context on failure."""
    try:
        return cast(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"{team_name}: field {field_name!r} is not a valid number: {raw_value!r}"
        ) from exc


def decode_streak(raw_value):
    """Decode Madden's byte-wrapped win/loss streak into a signed length.

    The Companion App export represents a losing streak as an unsigned
    byte: a 1-game losing streak comes across as 255, 2 games as 254, and
    so on (256 - n). Win streaks are stored as plain positive integers.
    Returns a positive int for a win streak, negative for a loss streak.
    """
    return raw_value if raw_value <= 127 else -(256 - raw_value)


def _parse_row(row):
    """Convert one raw CSV row (all string values) into a TeamRecord.

    Preconditions: every column in REQUIRED_COLUMNS must be present, every
    numeric field must parse, `winPct` must be a valid percentage, and
    `gamesPlayed` must be nonzero (a per-game stat would otherwise divide
    by zero later in analysis.py).
    """
    missing = REQUIRED_COLUMNS - row.keys()
    assert not missing, f"missing required columns: {sorted(missing)}"

    team_name = row["teamName"]
    fields = dict(row)
    for name in INT_FIELDS:
        fields[name] = _parse_number(row[name], name, team_name, int)
    for name in FLOAT_FIELDS:
        fields[name] = _parse_number(row[name], name, team_name, float)

    assert 0.0 <= fields["winPct"] <= 1.0, (
        f"{team_name}: winPct {fields['winPct']} is out of the valid 0-1 range"
    )
    assert fields["gamesPlayed"] > 0, f"{team_name}: gamesPlayed must be greater than 0"

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
    """Read the standings CSV at `path` and return {team_name: TeamRecord}.

    Precondition: the file must contain exactly EXPECTED_TEAM_COUNT teams
    (one row per NFL team) — a partial or duplicated export would silently
    skew every ranking downstream.
    """
    teams = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = _parse_row(row)
            teams[record.team_name] = record

    assert len(teams) == EXPECTED_TEAM_COUNT, (
        f"expected {EXPECTED_TEAM_COUNT} teams, found {len(teams)}"
    )
    return teams
