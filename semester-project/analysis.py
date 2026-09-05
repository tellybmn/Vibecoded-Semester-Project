"""Compute contender scores and compare them to the game's official rank."""

TURNOVER_POINT_VALUE = 4
YARDS_PER_POINT = 17
TREND_THRESHOLD = 3


def compute_contender_score(team):
    """Return a point-equivalent contender score for one team.

    Combines turnover margin and total-yardage margin, each normalized per
    game so a bye week doesn't penalize a team, using standard football
    analytics point-equivalency estimates (roughly 4 points per turnover of
    margin, and 17 yards per point).
    """
    turnover_margin_per_game = team.to_diff / team.games_played
    yard_margin_per_game = (team.off_total_yds - team.def_total_yds) / team.games_played
    return TURNOVER_POINT_VALUE * turnover_margin_per_game + yard_margin_per_game / YARDS_PER_POINT


def classify_trend(rank_gap):
    """Classify a rank gap as trending up, trending down, or steady.

    `rank_gap` is official rank minus contender rank: positive means the
    contender score says a team should rank better than its record shows
    (trending up); negative means the record is ahead of the underlying
    numbers (trending down).
    """
    if rank_gap >= TREND_THRESHOLD:
        return "TRENDING UP"
    if rank_gap <= -TREND_THRESHOLD:
        return "TRENDING DOWN"
    return "steady"


def rank_by_contender_score(teams):
    """Score, rank, and classify every team; return them sorted best-first.

    Fills in each TeamRecord's `contender_score`, `contender_rank`,
    `rank_gap`, and `trend` fields as a side effect.
    """
    for team in teams:
        team.contender_score = compute_contender_score(team)

    ranked = sorted(teams, key=lambda t: t.contender_score, reverse=True)
    for position, team in enumerate(ranked, start=1):
        team.contender_rank = position
        team.rank_gap = team.rank - team.contender_rank
        team.trend = classify_trend(team.rank_gap)
    return ranked


def biggest_rank_gaps(ranked_teams, count=8):
    """Return the `count` teams with the largest |official rank - contender rank|."""
    return sorted(ranked_teams, key=lambda t: abs(t.rank_gap), reverse=True)[:count]
