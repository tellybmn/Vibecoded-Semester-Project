"""Save contender-analysis charts to PNG using DataFrame .plot()."""

import matplotlib
matplotlib.use("Agg")  # no display available in this environment
import matplotlib.pyplot as plt


def save_top_contenders_chart(df, path, top_n=8):
    """Bar chart of the top `top_n` teams' contender scores, saved as a PNG."""
    top = df.head(top_n).set_index("teamName")
    ax = top["contenderScore"].plot(kind="bar", color="steelblue", figsize=(8, 5))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("")
    ax.set_ylabel("Contender score")
    ax.set_title(f"Top {top_n} projected contenders (week 6)")
    ax.figure.tight_layout()
    ax.figure.savefig(path)
    plt.close(ax.figure)


def save_yardage_vs_turnovers_chart(df, path):
    """Scatter of yardage margin/game vs. turnover differential, colored by playoff status."""
    ax = df.plot.scatter(
        x="tODiff",
        y="yardMarginPerGame",
        c="playoffStatus",
        cmap="coolwarm",
        figsize=(8, 6),
        colorbar=False,
    )
    ax.set_xlabel("Turnover differential")
    ax.set_ylabel("Yardage margin per game")
    ax.set_title("Yardage margin vs. turnover differential (red = in playoff position)")
    ax.figure.tight_layout()
    ax.figure.savefig(path)
    plt.close(ax.figure)
