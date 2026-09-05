"""Entry point: load standings, rank contenders, print and save the report."""

from data_loader import load_teams
from analysis import rank_by_contender_score
from report import build_report, save_report

DATA_FILE = "semester-project/phase0_dataset/ryze_cfm_madden27_2026_week6_standings.csv"
REPORT_FILE = "semester-project/week6_contender_report.txt"


def main():
    teams = load_teams(DATA_FILE)
    ranked = rank_by_contender_score(teams.values())

    report_text = build_report(ranked)
    print(report_text)
    save_report(report_text, REPORT_FILE)


if __name__ == "__main__":
    main()
