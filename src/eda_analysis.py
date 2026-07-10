# src/eda_analysis.py
import os
import pandas as pd


def load_dataset(file_path="data/final_enriched_bugfixes.csv"):
    if not os.path.exists(file_path):
        print(
            f" Error: Integrated dataset '{file_path}' not found. Run the pipeline integration first."
        )
        return None
    return pd.read_csv(file_path)


def generate_descriptive_stats(df):
    print("\n" + "=" * 20 + "  BASIC DESCRIPTIVE STATISTICS " + "=" * 20)

    lines_metrics = ["lines_added", "lines_deleted"]
    print("\n Code Change Metrics (Diff):")
    print(df[lines_metrics].describe().loc[["mean", "50%", "max", "std"]])

    complexity_metrics = ["avg_complexity", "max_complexity"]
    print("\n AST Complexity Metrics (Radon):")
    valid_cc = df[df["avg_complexity"].notna()]
    if not valid_cc.empty:
        print(
            valid_cc[complexity_metrics]
            .describe()
            .loc[["mean", "50%", "max", "std"]]
        )
    else:
        print(" No valid complexity data found to analyze.")


def analyze_critical_functions(df):
    print("\n" + "=" * 20 + "  CRITICAL FUNCTIONS ANALYSIS " + "=" * 20)

    total_high_funcs = df["high_complexity_functions_count"].sum()
    print(f"Total high-complexity functions modified: {total_high_funcs}")

    if total_high_funcs > 0:
        print("\n Top commits touching highly complex functions:")
        top_critical = df.sort_values(
            "high_complexity_functions_count", ascending=False
        ).head(5)
        print(
            top_critical[
                [
                    "commit_hash",
                    "repo_name",
                    "high_complexity_functions_count",
                    "max_complexity",
                ]
            ]
        )
    else:
        print(" Clean Code Notice: No high-complexity functions (> 5 CC) were found in these bug-fixes.")


def compute_correlations(df):
    print("\n" + "=" * 20 + "  STATISTICAL CORRELATION " + "=" * 20)

    df["total_lines_changed"] = df["lines_added"] + df["lines_deleted"]

    if (
        df["avg_complexity"].notna().sum() > 1
    ):  
        correlation = df["total_lines_changed"].corr(df["max_complexity"])
        print(
            f" Correlation between 'Total Lines Changed' and 'Max Complexity': {correlation:.2f}"
        )
        print(
            "> (Note: Closer to 1.0 means highly complex files require significantly larger bug-fix lines.)"
        )
    else:
        print(
            "ℹ Insight: Statistical correlation requires a larger history of commits to calculate variance."
        )


def main():
    print(" Loading final enriched dataset for Exploratory Data Analysis...")
    df = load_dataset()

    if df is None:
        return

    print(f" Dataset successfully loaded. Total bug-fix samples: {len(df)}")

    generate_descriptive_stats(df)
    analyze_critical_functions(df)
    compute_correlations(df)

    print("\n" + "=" * 55)
    print(" Advanced EDA completed successfully!")

if __name__ == "__main__":
    main()