# src/visualization.py
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_dataset(file_path="data/final_enriched_bugfixes.csv"):
    if not os.path.exists(file_path):
        print(f" Error: Dataset '{file_path}' not found.")
        return None
    return pd.read_csv(file_path)


def main():
    print(" Loading final enriched dataset for visualization...")
    df = load_dataset()

    if df is None:
        return

    df["lines_changed"] = df["lines_added"] + df["lines_deleted"]

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))
    if len(df) > 1:
        sns.histplot(data=df, x="lines_changed", bins=10, kde=True, color="blue")
    else:
        sns.barplot(data=df, x="commit_hash", y="lines_changed", color="blue")

    plt.title("Distribution of Bug-Fix Change Size", fontsize=14, pad=15)
    plt.xlabel("Lines Changed (Added + Deleted)", fontsize=12)
    plt.ylabel("Count / Lines", fontsize=12)
    plt.tight_layout()
    plt.show()

    repo_counts = df["repo_name"].value_counts().reset_index()
    repo_counts.columns = ["repo_name", "bugfix_count"]

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=repo_counts, x="repo_name", y="bugfix_count", palette="viridis"
    )

    plt.title("Number of Bug-Fix Commits per Repository", fontsize=14, pad=15)
    plt.xlabel("Repository Name", fontsize=12)
    plt.ylabel("Bug-Fix Commit Count", fontsize=12)
    plt.tight_layout()
    plt.show()

    print(" Visualizations generated successfully!")


if __name__ == "__main__":
    main()