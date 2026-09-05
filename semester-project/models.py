"""Data structures for a team's weekly standings record."""

from dataclasses import dataclass


@dataclass
class TeamRecord:
    """One team's row from the standings CSV, plus derived analysis fields.

    The raw fields come straight from the CSV (with numeric columns cast).
    The derived fields (`contender_score`, `contender_rank`, `rank_gap`,
    `trend`) start out unset and are filled in by `analysis.py` once every
    team has been loaded.
    """

    team_name: str
    conference_name: str
    division_name: str
    total_wins: int
    total_losses: int
    total_ties: int
    games_played: int
    win_pct: float
    to_diff: int
    off_total_yds: int
    off_pass_yds: int
    off_rush_yds: int
    def_total_yds: int
    def_pass_yds: int
    def_rush_yds: int
    team_ovr: int
    cap_room: int
    cap_available: int
    cap_spent: int
    rank: int
    seed: int
    playoff_status: int
    streak_length: int  # positive = win streak, negative = loss streak

    contender_score: float = None
    contender_rank: int = None
    rank_gap: int = None
    trend: str = None

    def format_streak(self):
        """Return the win/loss streak as a display string, e.g. 'W6' or 'L4'."""
        if self.streak_length >= 0:
            return f"W{self.streak_length}"
        return f"L{-self.streak_length}"

    def format_record(self):
        """Return the team's record as a display string, e.g. '5-1'."""
        return f"{self.total_wins}-{self.total_losses}"
