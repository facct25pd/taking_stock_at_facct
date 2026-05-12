import pandas as pd
from collections import Counter

pathrawclass = "TBD"
df = pd.read_csv(pathrawclass + "raw_theme_classification.csv")

annotator_cols = [
    "Opus 4.5",
    "Shiran",
    "Gemini 3 Pro",
    "Yanan",
    "GPT 5.2 thinking (agent mode)",
]


def get_majority_labels(row):
    all_labels = []
    for col in annotator_cols:
        cell = row[col]
        if pd.notna(cell) and cell.strip():
            labels = [
                l.strip().rstrip(";").strip() for l in str(cell).split(";") if l.strip()
            ]
            all_labels.extend(labels)

    # Normalize labels (handle minor spelling variations)
    normalized = []
    for label in all_labels:
        label_lower = label.lower()
        if "accessib" in label_lower or "inclusi" in label_lower:
            if "accessib" in label_lower:
                normalized.append("Inclusivity & Accessibility")
            else:
                normalized.append(label.title())
        else:
            normalized.append(label.title())

    # Count occurrences
    counts = Counter(normalized)

    # Majority = appears in 2+ of 3 annotators
    majority = [label for label, count in counts.items() if count >= 2]

    return "; ".join(sorted(majority)) if majority else ""


df["Majority"] = df.apply(get_majority_labels, axis=1)
df.to_csv(pathrawclass + "theme_classification.csv", index=False)
