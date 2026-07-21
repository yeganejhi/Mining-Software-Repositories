# src/visualization.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_dataset(file_path="data/final_enriched_bugfixes.csv"):
    if not os.path.exists(file_path):
        print(f"Dataset not found: {file_path}")
        return None

    return pd.read_csv(file_path)


def main():

    print("Loading dataset...")
    df = load_dataset()

    if df is None:
        return


    os.makedirs("plots", exist_ok=True)

    df["total_lines_changed"] = (
        df["lines_added"] + df["lines_deleted"]
    )


    sns.set_theme(style="whitegrid")


    # 1. Patch size distribution
    plt.figure(figsize=(8,5))

    sns.histplot(
        data=df,
        x="total_lines_changed",
        bins=20,
        kde=True
    )

    plt.title("Distribution of Bug-Fix Patch Size")
    plt.xlabel("Lines Changed")
    plt.ylabel("Number of Commits")

    plt.tight_layout()
    plt.savefig(
        "plots/patch_size_distribution.png",
        dpi=300
    )
    plt.close()



    # 2. Complexity distribution
    complexity_df = df.dropna(
        subset=["avg_complexity"]
    )

    if not complexity_df.empty:

        plt.figure(figsize=(8,5))

        sns.histplot(
            data=complexity_df,
            x="avg_complexity",
            bins=15,
            kde=True
        )

        plt.title(
            "Distribution of Average Cyclomatic Complexity"
        )

        plt.xlabel(
            "Average Complexity"
        )

        plt.ylabel(
            "Number of Commits"
        )

        plt.tight_layout()

        plt.savefig(
            "plots/complexity_distribution.png",
            dpi=300
        )

        plt.close()



    # 3. Churn vs Complexity
    if not complexity_df.empty:

        plt.figure(figsize=(8,5))

        sns.scatterplot(
            data=complexity_df,
            x="total_lines_changed",
            y="max_complexity",
            hue="repo_name",
            s=80
        )

        plt.title(
            "Code Churn vs Maximum Cyclomatic Complexity"
        )

        plt.xlabel(
            "Lines Changed"
        )

        plt.ylabel(
            "Maximum Complexity"
        )

        plt.tight_layout()

        plt.savefig(
            "plots/churn_vs_complexity.png",
            dpi=300
        )

        plt.close()



    # 4. Repository comparison
    repo_counts = (
        df["repo_name"]
        .value_counts()
        .reset_index()
    )

    repo_counts.columns = [
        "repo_name",
        "bugfix_count"
    ]


    plt.figure(figsize=(8,5))

    sns.barplot(
        data=repo_counts,
        x="repo_name",
        y="bugfix_count"
    )

    plt.title(
        "Bug-Fix Commits per Repository"
    )

    plt.xlabel(
        "Repository"
    )

    plt.ylabel(
        "Number of Bug-Fix Commits"
    )

    plt.tight_layout()

    plt.savefig(
        "plots/repository_bugfix_count.png",
        dpi=300
    )

    plt.close()



    # 5. Top complex commits
    if not complexity_df.empty:

        top_complex = (
            complexity_df
            .sort_values(
                "max_complexity",
                ascending=False
            )
            .head(10)
        )


        plt.figure(figsize=(10,5))

        sns.barplot(
            data=top_complex,
            x="commit_hash",
            y="max_complexity"
        )

        plt.xticks(
            rotation=75
        )

        plt.title(
            "Top 10 Bug-Fix Commits by Maximum Complexity"
        )

        plt.xlabel(
            "Commit Hash"
        )

        plt.ylabel(
            "Maximum Complexity"
        )

        plt.tight_layout()

        plt.savefig(
            "plots/top_complex_commits.png",
            dpi=300
        )

        plt.close()



    print("Visualization completed!")
    print("Plots saved in plots/ folder.")



if __name__ == "__main__":
    main()