import pandas as pd
import os

# Read both files
majority_df = pd.read_csv('/Users/shirandudy/Documents/Documents_new/NEU/projects/FAccT_co-design_2025/results/src/togit/fig7/theme_classification.csv')
votes_df = pd.read_csv('/Users/shirandudy/Documents/Documents_new/NEU/projects/FAccT_co-design_2025/results/csv/comment-groups.csv')

# Merge on comment-id
merged_df = pd.merge(
    majority_df[['comment-id', 'comment', 'Majority']],
    votes_df[['comment-id', 'total-votes', 'total-agrees', 'total-disagrees', 'total-passes']],
    on='comment-id',
    how='left'
)

# Function to generate interpretation based on voting patterns
def interpret_votes(row):
    total = row['total-votes']
    agrees = row['total-agrees']
    disagrees = row['total-disagrees']
    passes = row['total-passes']
    
    if pd.isna(total) or total == 0:
        return 'No votes recorded'
    
    agree_pct = (agrees / total) * 100
    disagree_pct = (disagrees / total) * 100
    pass_pct = (passes / total) * 100
    
    # Determine consensus level
    if agree_pct >= 75:
        consensus = 'Strong consensus agrees'
    elif disagree_pct >= 75:
        consensus = 'Strong consensus disagrees'
    elif agree_pct >= 50:
        consensus = 'Majority consensus'
    elif disagree_pct >= 50:
        consensus = 'Majority disagree'
    elif pass_pct >= 50:
        consensus = 'High uncertainty'
    else:
        consensus = 'Mixed opinions'
    
    # Determine engagement level
    if total >= 80:
        engagement = 'high engagement'
    elif total >= 50:
        engagement = 'moderate engagement'
    else:
        engagement = 'low engagement'
    
    return f"{consensus} ({agree_pct:.0f}% agree, {disagree_pct:.0f}% disagree, {pass_pct:.0f}% pass) - {engagement}"

# Add interpretation column
merged_df['interpretation'] = merged_df.apply(interpret_votes, axis=1)

# Get all unique themes
all_themes = set()
for majority in merged_df['Majority'].dropna():
    themes = [t.strip() for t in str(majority).split(';') if t.strip()]
    all_themes.update(themes)

print(f"Found {len(all_themes)} unique themes:")
for theme in sorted(all_themes):
    print(f"  - {theme}")

# Create output directory
output_dir = '/Users/shirandudy/Documents/Documents_new/NEU/projects/FAccT_co-design_2025/results/src/togit/section_4.3/votes_by_themes'
os.makedirs(output_dir, exist_ok=True)

# Generate a CSV for each theme
for theme in sorted(all_themes):
    # Filter rows that contain this theme
    theme_mask = merged_df['Majority'].apply(
        lambda x: theme in str(x) if pd.notna(x) else False
    )
    theme_df = merged_df[theme_mask].copy()
    
    # Select and order columns
    output_df = theme_df[[
        'comment-id', 
        'comment', 
        'total-votes', 
        'total-agrees', 
        'total-disagrees', 
        'total-passes',
        'interpretation'
    ]]
    
    # Create safe filename
    safe_filename = theme.replace(' ', '_').replace('&', 'and').replace('/', '_')
    filepath = os.path.join(output_dir, f"{safe_filename}.csv")
    
    # Save to CSV
    output_df.to_csv(filepath, index=False)
    print(f"\nCreated: {safe_filename}.csv ({len(output_df)} comments)")
    print(output_df[['comment-id', 'interpretation']].head(3).to_string(index=False))

print(f"\n✓ All {len(all_themes)} themed CSV files saved to {output_dir}")