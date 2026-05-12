### Figure 4

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

# Load data
path2pvotes = TBD
pvotes = pd.read_csv(path2pvotes + 'participant-votes.csv')

# rm filtered comments
pvotes = pvotes.drop('45', axis=1)
pvotes = pvotes.drop('47', axis=1)

# Read the CSV file
#df = pd.read_csv('participantvotes.csv')
colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33']

# Filter for rows where n-comments > 1
filtered_df = pvotes[pvotes['n-comments'] > 0].copy()

# Calculate average n-votes for baseline
avg_votes = filtered_df['n-votes'].mean()
avg_votes_all = pvotes['n-votes'].mean()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot n-comments and n-votes for each participant
participants = filtered_df['participant'].values[1:]
n_comments = filtered_df['n-comments'].values[1:]
n_votes = filtered_df['n-votes'].values[1:]

# Create bar plot for n-comments (primary y-axis)
bars = ax.bar(range(len(participants)), n_comments, alpha=0.6, label='n-comments', color=colors[0])

# Add n-comments values above each bar
for i, (bar, value) in enumerate(zip(bars, n_comments)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(value), ha='center', va='bottom', fontsize=10, fontweight='bold')
# Create scatter plot for n-votes on the same axis
ax.scatter(range(len(participants)), n_votes, color=colors[1], s=100, label='n-votes', zorder=3)

# Add horizontal line for average n-votes
ax.axhline(y=avg_votes_all, color=colors[3], linestyle='--', linewidth=2, label=f'Avg votes per participant (35.5)')#{avg_votes_all:.1f}


# Customize the plot
ax.set_xlabel('Participant ID', fontsize=20)
ax.set_ylabel('Count', fontsize=20)
ax.set_title('Comments and Votes per Comment-Maker Participants (n-comments > 0)', fontsize=22)
ax.set_xticks(range(len(participants)))
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

ax.set_xticklabels(participants, rotation=45, ha='right')
# to set the font size of the legend
ax.legend(loc='upper left', fontsize=15)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
path2save = TBD
plt.savefig(path2save+"comment_makers.pdf", bbox_inches='tight')
plt.show()

# Print summary statistics
print(f"Number of participants with n-comments > 0: {len(filtered_df)}")
print(f"Average n-votes: {avg_votes:.2f}")
print(f"Average n-votes all: {avg_votes_all:.2f}")
print(f"\nParticipant details:")
print(filtered_df[['participant', 'n-comments', 'n-votes']].to_string(index=False))
