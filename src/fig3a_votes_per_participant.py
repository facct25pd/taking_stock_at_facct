### Figure 3(a)

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

# Load data
path2votes = TBD
votes_unflitered = pd.read_csv(path2votes+'votes.csv')

colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33']
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC']

# rm filtered comments
votes_a = votes_unflitered[votes_unflitered["comment-id"]!=45]
votes = votes_a[votes_a["comment-id"]!=47]

# shift the last comments to occupy the empty slots
votes["comment-id"] = votes["comment-id"].replace(59,45)
votes["comment-id"] = votes["comment-id"].replace(60,47)

# Count votes per voter
votes_per_voter = votes.groupby('voter-id').size().reset_index(name='vote_count')

# Sort by vote count in descending order
votes_per_voter = votes_per_voter.sort_values('vote_count', ascending=True).reset_index(drop=True)

# Create x-axis as rank (1, 2, 3, ...)
votes_per_voter['rank'] = range(1, len(votes_per_voter) + 1)

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot as bar chart
ax.scatter(votes_per_voter['rank'], votes_per_voter['vote_count'], color=colors[3], s=100, label='n-votes', zorder=3)

# Labels
ax.set_xlabel('Voter Rank (sorted by votes cast)', fontsize=25)
ax.set_ylabel('Number of Votes Cast', fontsize=25)
ax.set_title('Votes Cast per Participant (Ascending Order)', fontsize=25)#, fontweight='bold')
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)

# Add average line
avg_votes = votes_per_voter['vote_count'].mean()
ax.axhline(y=avg_votes, color='#377EB8', linestyle='--', linewidth=2, label=f'Average: {avg_votes:.1f} votes')
ax.legend(fontsize=15)

# Add median line
avg_votes = votes_per_voter['vote_count'].median()
ax.axhline(y=avg_votes, color='olive', linestyle='--', linewidth=2, label=f'Median: {avg_votes:.1f} votes')
ax.legend(fontsize=15)

# Adjust layout
plt.tight_layout()

# Save
path2save = TBD
plt.savefig(path2save+'votes_per_voter.pdf', bbox_inches='tight')
