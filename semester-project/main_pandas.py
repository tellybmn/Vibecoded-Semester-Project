"""Phase 4 entry point: pandas + matplotlib recreation of the contender analysis."""

from pandas_analysis import load_standings, add_contender_score, top_contenders, biggest_rank_gaps
from pandas_charts import save_top_contenders_chart, save_yardage_vs_turnovers_chart

DATA_FILE = "semester-project/phase0_dataset/ryze_cfm_madden27_2026_week6_standings.csv"
REPORT_FILE = "semester-project/week6_contender_report_pandas.csv"
TOP_CHART_FILE = "semester-project/top_contenders_chart.png"
SCATTER_CHART_FILE = "semester-project/yardage_vs_turnovers_chart.png"

REPORT_COLUMNS = [
    "contenderRank", "teamName", "contenderScore",
    "totalWins", "totalLosses", "rank", "rankGap", "trend",
]


def main():
    df = load_standings(DATA_FILE)
    df = add_contender_score(df)

    print("Top 8 projected true contenders (by contender score):")
    print(top_contenders(df)[REPORT_COLUMNS].to_string(index=False))

    print("\nBiggest gaps between contender score rank and official rank:")
    print(biggest_rank_gaps(df)[REPORT_COLUMNS].to_string(index=False))

    df[REPORT_COLUMNS].to_csv(REPORT_FILE, index=False)
    save_top_contenders_chart(df, TOP_CHART_FILE)
    save_yardage_vs_turnovers_chart(df, SCATTER_CHART_FILE)
    print(f"\nSaved report to {REPORT_FILE}")
    print(f"Saved charts to {TOP_CHART_FILE} and {SCATTER_CHART_FILE}")


if __name__ == "__main__":
    main()
