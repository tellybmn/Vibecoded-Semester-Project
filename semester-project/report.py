"""Format and save the week-6 contender report."""

from analysis import biggest_rank_gaps


def _format_team_line(team):
    """Format one team's line for the top-contenders section."""
    return (
        f"  #{team.contender_rank:>2} {team.team_name:<12} "
        f"score={team.contender_score:+6.2f}  "
        f"record={team.format_record()} "
        f"({team.format_streak()})  "
        f"official rank={team.rank:>2}  {team.trend}"
    )


def _format_gap_line(team):
    """Format one team's line for the biggest-gaps section."""
    return (
        f"  {team.team_name:<12} contender rank={team.contender_rank:>2}  "
        f"official rank={team.rank:>2}  gap={team.rank_gap:+3}  {team.trend}"
    )


def build_report(ranked_teams, top_n=8, gap_n=8):
    """Build the full report text: top contenders, then biggest rank gaps."""
    lines = ["=== Week 6 Contender Report ===", ""]

    lines.append(f"Top {top_n} projected true contenders (by contender score):")
    lines.extend(_format_team_line(t) for t in ranked_teams[:top_n])

    lines.append("")
    lines.append("Biggest gaps between contender score rank and official rank:")
    lines.extend(_format_gap_line(t) for t in biggest_rank_gaps(ranked_teams, gap_n))

    return "\n".join(lines)


def save_report(text, path):
    """Write report text to `path`, with a trailing newline."""
    with open(path, "w") as f:
        f.write(text + "\n")
