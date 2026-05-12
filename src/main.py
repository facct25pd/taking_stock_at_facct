import runpy
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "fig3a_votes_per_participant.py",
    "fig3b_votes_distribution.py",
    "fig4_commentmaker_votes.py",
    # TODO (missing comment-groups.csv): "fig5a_votes_by_statement_order.py",
    "fig5b_participation_duration.py",
    "fig6_normative_descriptive_classification.py",
    "fig7/create_final_theme_classification.py",
    "fig7/fig7_themes.py",
    # TODO (missing comment-groups.csv): "section4.3/votes_analysis_by_theme.py",
]


def main():
    for script in SCRIPTS:
        script_path = SRC_DIR / script
        print(f"Running {script}...")
        runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
