import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
from collections import Counter
import seaborn as sns


# Read the Majority column from the Excel file
path2themes = TBD
df = pd.read_csv(path2themes+'theme_classification.csv')

# Extract non-empty Majority values as raw_data
raw_data = df['Majority'].dropna().tolist()
raw_data = [item for item in raw_data if str(item).strip()]  # Remove empty strings

# Parse the data and clean up inconsistencies
def parse_labels(text):
    text = text.replace(';', ',')
    labels = [label.strip() for label in text.split(',') if label.strip()]
    normalized = []
    for label in labels:
        normalized.append(label.title())
    return normalized

# Convert to list of all themes
memberships = [parse_labels(item) for item in raw_data]
all_themes = [theme for membership in memberships for theme in membership]

# Count theme frequencies
theme_counts = Counter(all_themes)
sorted_themes = theme_counts.most_common()

# Define a color palette from seaborn
colors = sns.color_palette("tab20", n_colors=len(sorted_themes)).as_hex()

# Create individual waffle plots in a 4x4 grid
print("Creating 4x4 grid of waffle plots for each theme...\n")

n_cols = 6
n_rows = 4
total_plots = n_cols * n_rows

# Create a large figure with subplots
fig = plt.figure(figsize=(20, 20))

for idx, (theme, count) in enumerate(sorted_themes[:total_plots]):  # Limit to 16 themes
    # Calculate subplot position (1-indexed for matplotlib)
    subplot_idx = idx + 1
    
    # Create waffle plot in this subplot position
    ax = fig.add_subplot(
        n_rows, n_cols, subplot_idx,
        aspect='equal'
    )
    
    # Calculate grid dimensions for waffle
    waffle_rows = 5
    waffle_cols = (count + waffle_rows - 1) // waffle_rows
    
    # Manually create waffle chart
    # Create a grid of squares
    for i in range(count):
        row = i // waffle_cols
        col = i % waffle_cols
        ax.add_patch(plt.Rectangle((col, waffle_rows - row - 1), 0.9, 0.9, 
                                   facecolor=colors[idx % len(colors)], 
                                   edgecolor='white', linewidth=2))
    
    # Set limits and remove axes
    ax.set_xlim(-0.5, waffle_cols + 0.5)
    ax.set_ylim(-0.5, waffle_rows + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title
    if '&' in theme:
        a, b = theme.split('&')
        theme = a+"&\n"+b
    if "Environmental Sustainability" in theme:
        theme = "Environmental\nSustainability"
    if "Industry Engagement" in theme:
        theme = "Industry\nEngagement"
    if count == 1:
        ax.set_title(f'{theme}\n({count} statement)', 
            fontsize=20, fontweight='bold', pad=10)
    else:
        ax.set_title(f'{theme}\n({count} statements)', 
            fontsize=20, fontweight='bold', pad=10)

plt.tight_layout()

path2save = TBD
plt.savefig(path2save+'facct_themes.pdf', bbox_inches='tight')