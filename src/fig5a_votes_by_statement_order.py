### Figure 5(a)

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from paths import POLIS_DATA_DIR, FIGURES_DIR, LABELS_DATA_DIR


def parse_datetime(datetime_str):
    try:
        datetime_str_clean = datetime_str.split(" (")[0]
        return datetime.strptime(datetime_str_clean, "%a %b %d %Y %H:%M:%S GMT%z")
    except Exception as e:
        print(f"Error parsing: {datetime_str}, Error: {e}")
        return None


# Read both CSV files
comments_df = pd.read_csv(POLIS_DATA_DIR / "comments.csv")
commentgroups_df = pd.read_csv(LABELS_DATA_DIR / "comment-groups.csv")

# rm filtered comments
comments_df = comments_df[comments_df["comment-id"] != 45]
comments_df = comments_df[comments_df["comment-id"] != 47]

commentgroups_df = commentgroups_df[commentgroups_df["comment-id"] != 45]
commentgroups_df = commentgroups_df[commentgroups_df["comment-id"] != 47]

# Parse datetime
comments_df["datetime"] = pd.to_datetime(comments_df["datetime"].apply(parse_datetime))

# Merge to get datetime and total-votes together
merged_df = comments_df[["comment-id", "datetime"]].merge(
    commentgroups_df[["comment-id", "total-votes"]], on="comment-id"
)

# Sort by datetime and create submission order
merged_df = merged_df.sort_values("datetime").reset_index(drop=True)
merged_df["submission_order"] = range(1, len(merged_df) + 1)

# Create the plot
fig, ax = plt.subplots(figsize=(14, 9))

# Plot as bar chart
ax.bar(
    merged_df["submission_order"], merged_df["total-votes"], color="#FF7F00", alpha=0.5
)

below_90 = merged_df[merged_df["total-votes"] < 90]
first_below_90 = below_90.iloc[0] if len(below_90) > 0 else None
date_str = first_below_90["datetime"].strftime("%b %d, %Y")


# Add average line
avg_votes = merged_df["total-votes"].mean()
ax.axhline(
    y=avg_votes,
    color="teal",
    linestyle="--",
    linewidth=2,
    label=f"Average: {avg_votes:.1f} votes",
)

# Add median line
med_votes = merged_df["total-votes"].median()
ax.axhline(
    y=med_votes,
    color="darkmagenta",
    linestyle="--",
    linewidth=2,
    label=f"Median: {med_votes:.1f} votes",
)

# Labels
ax.set_xlabel("Statement (ordered by submission date)", fontsize=30)
ax.set_ylabel("Total Votes", fontsize=30)
ax.set_title(
    "Total Votes per Statement by Submission Order", fontsize=30
)  # , fontweight='bold')
ax.legend(fontsize=20, loc="lower center")
ax.grid(axis="y", alpha=0.6)

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "statement_votes_by_submission_order.pdf", bbox_inches="tight"
)
plt.show()

# Print summary statistics
print(f"Total statements: {len(merged_df)}")
print(f"Average votes per statement: {avg_votes:.1f}")
print(f"Max votes: {merged_df['total-votes'].max()}")
print(f"Min votes: {merged_df['total-votes'].min()}")
