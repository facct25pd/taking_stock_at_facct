### Figure 6

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.colors as mcolors


# Load the CSV file
path2statementclass = "TBD"

df = pd.read_csv(path2statementclass + "normative_descriptive_classification.csv")


def classify_statement_subtype(row):
    """
    Classify statements into detailed subtypes based on their prefix and type

    Args:
        row: DataFrame row with 'comment' and 'Statement_Type' columns

    Returns:
        Statement subtype string
    """
    comment = row["comment"]
    statement_type = row["Statement_Type"]
    c_id = row["comment-id"]

    if pd.isna(comment):
        return "Unknown"

    comment_lower = comment.lower().strip()

    # Only classify if we know it's Normative
    if statement_type == "Normative":
        if "should not" in comment_lower or "shouldn't" in comment_lower:
            return "FAccT should NOT"
        elif "should" in comment_lower:
            return "FAccT should"
        else:
            return "Other normative"

    # Only classify if we know it's Descriptive
    elif statement_type == "Descriptive":
        if "is not" in comment_lower or "isn't" in comment_lower:
            return "FAccT is NOT"
        elif " is " in comment_lower or comment_lower.startswith("is "):
            return "FAccT is"
        else:
            return "Other descriptive"

    else:
        return "Other"


# Apply to each row (axis=1 means row-wise)
df["Statement_Subtype"] = df.apply(classify_statement_subtype, axis=1)

# Filter out Unknown statements
print(f"Original total statements: {len(df)}")
unknown_count = df[df["Statement_Type"] == "Unknown"].shape[0]
print(f"Unknown statements (filtered out): {unknown_count}")

df_filtered = df[df["Statement_Type"] != "Unknown"].copy()
print(f"Statements after filtering: {len(df_filtered)}\n")

# Count statements by type (using filtered data)
counts = (
    df_filtered.groupby(["Statement_Type", "Statement_Subtype"])
    .size()
    .reset_index(name="count")
)

# Calculate totals (using filtered data)
total_statements = len(df_filtered)
normative_total = df_filtered[df_filtered["Statement_Type"] == "Normative"].shape[0]
descriptive_total = df_filtered[df_filtered["Statement_Type"] == "Descriptive"].shape[0]
other_total = df_filtered[df_filtered["Statement_Type"] == "Other"].shape[0]

print("=== Statement Distribution ===")
print(f"Total Statements: {total_statements}")
print(f"Normative: {normative_total}")
print(f"Descriptive: {descriptive_total}")
print(f"Other: {other_total}")
print("\nDetailed breakdown:")
print(counts)

root_color = "#F0F0F0"
normative_base = "#E69F00"  # Orange
descriptive_base = "#56B4E9"  # Sky blue
other_base = "#999999"


# Function to adjust color intensity based on proportion
def get_color_by_intensity(base_color, value, max_value, min_intensity=0.3):
    """
    Adjust color intensity based on relative value.
    Higher values get more saturated colors.

    Args:
        base_color: hex color string
        value: count for this category
        max_value: maximum count in this group
        min_intensity: minimum intensity (0-1), prevents colors from being too light
    """
    if max_value == 0:
        return base_color

    # Calculate intensity (0 to 1)
    intensity = min_intensity + (1 - min_intensity) * (value / max_value)

    # Convert hex to RGB
    rgb = mcolors.hex2color(base_color)

    # Adjust saturation/lightness
    # Mix with white to reduce intensity
    adjusted_rgb = tuple(intensity * c + (1 - intensity) * 1.0 for c in rgb)

    return mcolors.rgb2hex(adjusted_rgb)


# Calculate max values for each group (for color scaling)
normative_max = counts[counts["Statement_Type"] == "Normative"]["count"].max()
descriptive_max = counts[counts["Statement_Type"] == "Descriptive"]["count"].max()

# Create the tree visualization
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis("off")

# Define positions for nodes
positions = {
    "root": (9, 8.5),
    "normative": (4.5, 6),
    "descriptive": (13.5, 6),
    "other": (9, 6),  # Or position at (16.5, 6) if you want it far right
}

# Normative subcategories - side by side at same level
normative_subs = ["FAccT should", "FAccT should NOT", "Other normative"]
norm_x_positions = [2, 4.5, 7]  # Spread horizontally
for i, sub in enumerate(normative_subs):
    positions[sub] = (norm_x_positions[i], 3.5)  # Same y-coordinate

# Descriptive subcategories - side by side at same level
descriptive_subs = ["FAccT is", "FAccT is NOT", "Other descriptive"]
desc_x_positions = [10.5, 13.5, 16.5]  # Spread horizontally
for i, sub in enumerate(descriptive_subs):
    positions[sub] = (desc_x_positions[i], 3.5)  # Same y-coordinate


# Helper function to draw a node
def draw_node(
    ax, pos, text, count=None, box_color="lightblue", text_size=10, box_width=1.2
):
    if count is not None:
        if text == "All Statements":
            label = f"{text}\n(59)"
        else:
            label = f"{text}"
    else:
        label = text

    bbox = FancyBboxPatch(
        (pos[0] - box_width / 2, pos[1] - 0.5),
        box_width,
        1.2,
        boxstyle="round,pad=0.05",
        edgecolor="black",
        facecolor=box_color,
        linewidth=2,
        zorder=2,
    )  # Add zorder=2 for boxes
    ax.add_patch(bbox)
    ax.text(
        pos[0],
        pos[1],
        label,
        ha="center",
        va="center",
        fontsize=text_size,
        fontweight="bold",
        zorder=3,
    )  # Add zorder=3 for text


# Helper function to draw edge with count
def draw_edge(ax, pos1, pos2, count, offset_x=0, offset_y=0):
    # Draw line with zorder=1 (behind boxes)
    ax.plot(
        [pos1[0], pos2[0]],
        [pos1[1] - 0.25, pos2[1] + 0.25],
        "k-",
        linewidth=2,
        alpha=0.6,
        zorder=1,
    )

    # Calculate midpoint for label
    mid_x = (pos1[0] + pos2[0]) / 2 + offset_x
    mid_y = (pos1[1] + pos2[1]) / 2 + offset_y

    # Draw count label on edge
    ax.text(
        mid_x,
        mid_y,
        f"n={count}",
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8
        ),
        fontsize=16,
        fontweight="bold",
        zorder=2,
    )


# FIRST: Draw all edges (in the background, zorder=1)
# Draw edges from root to level 1
draw_edge(ax, positions["root"], positions["normative"], normative_total, offset_x=-0.5)
draw_edge(
    ax, positions["root"], positions["descriptive"], descriptive_total, offset_x=0.5
)
draw_edge(ax, positions["root"], positions["other"], other_total, offset_x=0)

# Draw edges from normative to its subcategories
for sub in normative_subs:
    sub_count = counts[
        (counts["Statement_Type"] == "Normative") & (counts["Statement_Subtype"] == sub)
    ]["count"].sum()
    if sub_count > 0:
        draw_edge(ax, positions["normative"], positions[sub], sub_count)

# Draw edges from descriptive to its subcategories
for sub in descriptive_subs:
    sub_count = counts[
        (counts["Statement_Type"] == "Descriptive")
        & (counts["Statement_Subtype"] == sub)
    ]["count"].sum()
    if sub_count > 0:
        draw_edge(ax, positions["descriptive"], positions[sub], sub_count)

# Draw the 'Other' category node
if other_total > 0:
    draw_node(
        ax,
        positions["other"],
        "Other",
        other_total,
        box_color=other_base,
        text_size=16,
        box_width=1.3,
    )

# SECOND: Draw all nodes (in the foreground, zorder=2-3)
# Draw root node
draw_node(
    ax,
    positions["root"],
    "All Statements",
    total_statements,
    box_color=root_color,
    text_size=16,
    box_width=2,
)

# Draw level 1 nodes (Normative/Descriptive)
draw_node(
    ax,
    positions["normative"],
    "Normative",
    normative_total,
    box_color=normative_base,
    text_size=16,
    box_width=1.7,
)
draw_node(
    ax,
    positions["descriptive"],
    "Descriptive",
    descriptive_total,
    box_color=descriptive_base,
    text_size=16,
    box_width=1.7,
)

# Draw normative subcategories (nodes only, edges later)
for sub in normative_subs:
    sub_count = counts[
        (counts["Statement_Type"] == "Normative") & (counts["Statement_Subtype"] == sub)
    ]["count"].sum()

    if sub_count > 0:
        # Adjust box width for longer text
        color = get_color_by_intensity(normative_base, sub_count, normative_max)
        if "NOT" in sub:
            box_w = 2.4
        elif "should" in sub:
            box_w = 1.7
        else:
            box_w = 2.2
        draw_node(
            ax,
            positions[sub],
            sub,
            sub_count,
            box_color=color,
            text_size=16,
            box_width=box_w,
        )

# Draw descriptive subcategories (nodes only, edges later)
for sub in descriptive_subs:
    sub_count = counts[
        (counts["Statement_Type"] == "Descriptive")
        & (counts["Statement_Subtype"] == sub)
    ]["count"].sum()

    if sub_count > 0:
        color = get_color_by_intensity(descriptive_base, sub_count, descriptive_max)
        # Adjust box width for longer text
        if "NOT" in sub:
            box_w = 1.7
        elif "is" in sub:
            box_w = 1.2
        else:
            box_w = 2.2
        draw_node(
            ax,
            positions[sub],
            sub,
            sub_count,
            box_color=color,
            text_size=16,
            box_width=box_w,
        )

plt.tight_layout()

# Save the figure
path2save = "/Users/shirandudy/Documents/Documents_new/NEU/projects/FAccT_co-design_2025/results/figs/"
plt.savefig(path2save + "statement_tree.pdf", bbox_inches="tight", facecolor="white")
