### Figure 5(b)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

from paths import POLIS_DATA_DIR, FIGURES_DIR

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

# Load the data
df = pd.read_csv(POLIS_DATA_DIR / "votes.csv")

# Convert timestamp to datetime
df["vote_time"] = pd.to_datetime(df["timestamp"], unit="s")

# Calculate voting duration for each participant (voter-id)
participant_stats = (
    df.groupby("voter-id")
    .agg(
        first_vote=("vote_time", "min"),
        last_vote=("vote_time", "max"),
        vote_count=("vote_time", "count"),
    )
    .reset_index()
)

# Calculate duration in minutes
participant_stats["duration_minutes"] = (
    participant_stats["last_vote"] - participant_stats["first_vote"]
).dt.total_seconds() / 60

# Filter participants with duration > 30 minutes
filtered_participants = participant_stats[
    participant_stats["duration_minutes"] > 30
].copy()

print(f"Total participants: {len(participant_stats)}")
print(f"Participants with >30 min duration: {len(filtered_participants)}")
print("\nFiltered participants summary:")
print(
    filtered_participants[
        ["voter-id", "first_vote", "last_vote", "duration_minutes"]
    ].to_string()
)

# Sort participants by their first vote time for better visualization
filtered_participants_sorted = filtered_participants.sort_values(
    "first_vote", ascending=False
)

# Create the plot
fig, ax = plt.subplots(figsize=(14, 10))


# Color map for different 30-minute intervals based on duration
max_duration = filtered_participants["duration_minutes"].max()
norm = plt.Normalize(0, max_duration)
cmap = plt.cm.viridis

# Plot horizontal lines for each participant
y_positions = range(len(filtered_participants_sorted))
for idx, (_, row) in enumerate(filtered_participants_sorted.iterrows()):
    color = "olivedrab"  # (norm(row['duration_minutes']))

    # Draw the horizontal line from first to last vote
    ax.hlines(
        y=idx,
        xmin=row["first_vote"],
        xmax=row["last_vote"],
        colors=color,
        linewidths=4,
        alpha=0.8,
    )

    # Add markers for start and end points
    ax.scatter(
        [row["first_vote"]],
        [idx],
        color=color,
        s=80,
        zorder=5,
        edgecolors="white",
        linewidths=1,
    )
    ax.scatter(
        [row["last_vote"]],
        [idx],
        color=color,
        s=80,
        zorder=5,
        edgecolors="white",
        linewidths=1,
        marker="s",
    )

# Customize the plot
ax.set_yticks(y_positions)
ax.set_yticklabels([f"{pid}" for pid in filtered_participants_sorted["voter-id"]])

# Key dates
key_dates = [
    datetime(2025, 6, 26),
    datetime(2025, 6, 29),
    datetime(2025, 7, 18),
    datetime(2025, 7, 31),
]
date_labels = [
    "Jun 26\n(CRAFT)",
    "Jun 29\n(Online)",
    "Jul 18\n(Reminder 1)",
    "Jul 31\n(Reminder 2)",
]

# Add vertical lines for key dates
for date, label in zip(key_dates, date_labels):
    ax.axvline(x=date, color="dimgray", linestyle="--", alpha=0.7)
    ax.text(
        date, ax.get_ylim()[1] * 1.02, label, ha="center", fontsize=17, color="dimgray"
    )


# Format x-axis as dates
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

# Rotate date labels for better readability
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Participant ID", fontsize=20)
ax.set_title(
    "Participation Duration Timeline for Participants with >30 Minutes on Platform",
    fontsize=25,
    y=1.14,
)

# Add grid
ax.grid(axis="x", alpha=0.3, linestyle="--")
ax.grid(axis="y", alpha=0.2)
ax.tick_params(axis="y", labelcolor="black", labelsize=25)
ax.tick_params(axis="x", labelcolor="black", labelsize=25)

# Expand x-axis slightly for better visibility
x_margin = timedelta(hours=12)
ax.set_xlim(
    filtered_participants["first_vote"].min() - x_margin,
    filtered_participants["last_vote"].max() + x_margin,
)

plt.tight_layout()

plt.savefig(FIGURES_DIR / "voting_timeline.pdf", bbox_inches="tight")
