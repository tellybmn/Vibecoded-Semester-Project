import csv

DATA_FILE = "semester-project/phase0_dataset/ryze_cfm_madden27_2026_week6_standings.csv"
REPORT_FILE = "semester-project/week6_contender_report.txt"

INT_FIELDS = [
    "totalWins", "totalLosses", "totalTies", "gamesPlayed", "tODiff",
    "offTotalYds", "offPassYds", "offRushYds",
    "defTotalYds", "defPassYds", "defRushYds",
    "teamOvr", "capRoom", "capAvailable", "capSpent",
    "rank", "seed", "playoffStatus",
]
FLOAT_FIELDS = ["winPct"]

TURNOVER_POINT_VALUE = 4
YARDS_PER_POINT = 17
TREND_THRESHOLD = 3


def load_teams(path):
    teams = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = dict(row)
            for field in INT_FIELDS:
                team[field] = int(row[field])
            for field in FLOAT_FIELDS:
                team[field] = float(row[field])

            # Madden's export wraps a losing streak as an unsigned byte:
            # 255 -> a 1-game losing streak, 254 -> 2 games, and so on.
            raw_streak = int(row["winLossStreak"])
            team["streakLength"] = raw_streak if raw_streak <= 127 else -(256 - raw_streak)

            teams[team["teamName"]] = team
    return teams


def format_streak(streak_length):
    if streak_length >= 0:
        return f"W{streak_length}"
    return f"L{-streak_length}"


def main():
    teams = load_teams(DATA_FILE)

    for team in teams.values():
        games = team["gamesPlayed"]
        turnover_margin_per_game = team["tODiff"] / games
        yard_margin_per_game = (team["offTotalYds"] - team["defTotalYds"]) / games
        team["contenderScore"] = (
            TURNOVER_POINT_VALUE * turnover_margin_per_game + yard_margin_per_game / YARDS_PER_POINT
        )

    ranked = sorted(teams.values(), key=lambda t: t["contenderScore"], reverse=True)
    for i, team in enumerate(ranked, start=1):
        team["contenderRank"] = i
        team["rankGap"] = team["rank"] - team["contenderRank"]
        if team["rankGap"] >= TREND_THRESHOLD:
            team["trend"] = "TRENDING UP"
        elif team["rankGap"] <= -TREND_THRESHOLD:
            team["trend"] = "TRENDING DOWN"
        else:
            team["trend"] = "steady"

    top_8 = ranked[:8]
    biggest_gaps = sorted(teams.values(), key=lambda t: abs(t["rankGap"]), reverse=True)[:8]

    lines = []
    lines.append("=== Week 6 Contender Report ===")
    lines.append("")
    lines.append("Top 8 projected true contenders (by contender score):")
    for team in top_8:
        lines.append(
            f"  #{team['contenderRank']:>2} {team['teamName']:<12} "
            f"score={team['contenderScore']:+6.2f}  "
            f"record={team['totalWins']}-{team['totalLosses']} "
            f"({format_streak(team['streakLength'])})  "
            f"official rank={team['rank']:>2}  {team['trend']}"
        )

    lines.append("")
    lines.append("Biggest gaps between contender score rank and official rank:")
    for team in biggest_gaps:
        lines.append(
            f"  {team['teamName']:<12} contender rank={team['contenderRank']:>2}  "
            f"official rank={team['rank']:>2}  gap={team['rankGap']:+3}  {team['trend']}"
        )

    report_text = "\n".join(lines)
    print(report_text)

    with open(REPORT_FILE, "w") as f:
        f.write(report_text + "\n")


if __name__ == "__main__":
    main()
