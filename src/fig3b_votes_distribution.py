### Figure 3(b)

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif" 
plt.rcParams["font.serif"] = ["Times New Roman"]

# Load data
path2votes = TBD
votes = pd.read_csv(path2votes + 'votes.csv')

# rm filtered comments
votes = votes[votes["comment-id"]!=45]
votes = votes[votes["comment-id"]!=47]

# Count votes by type
vote_counts = votes['vote'].value_counts().sort_index()

# Prepare data for donut chart
labels = ['Disagree (-1)', 'Pass (0)', 'Agree (+1)']
sizes = [vote_counts[-1], vote_counts[0], vote_counts[1]]
colors = ['crimson', '#999999', 'olivedrab']  # Red, Gray, Green
explode = (0.02, 0.02, 0.02)  # Slight separation

# Calculate percentages
total = sum(sizes)
percentages = [s/total*100 for s in sizes]

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Create donut chart
wedges, texts, autotexts = ax.pie(sizes, 
                                   labels=labels,
                                   colors=colors,
                                   explode=explode,
                                   autopct='%1.1f%%',
                                   startangle=110,
                                   pctdistance=0.75,
                                   wedgeprops=dict(width=0.5, edgecolor='white'))

# Style the text
for autotext in autotexts:
    autotext.set_fontsize(24)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

for text in texts:
    text.set_fontsize(25)

# Add center text
center_text = f'Total\n{total:,}\nvotes'
ax.text(0, 0, center_text, ha='center', va='center', fontsize=25)# , fontweight='bold'

# Equal aspect ratio ensures circular shape
ax.axis('equal')

plt.tight_layout()

# Save
path2save = TBD
plt.savefig(path2save + 'vote_distribution_donut.pdf', bbox_inches='tight')
print("Plot saved successfully!")

# Print summary
print(f"\nVote Distribution:")
print(f"  Agree (+1):    {sizes[2]:,} ({percentages[2]:.1f}%)")
print(f"  Pass (0):      {sizes[1]:,} ({percentages[1]:.1f}%)")
print(f"  Disagree (-1): {sizes[0]:,} ({percentages[0]:.1f}%)")
print(f"  Total:         {total:,}")