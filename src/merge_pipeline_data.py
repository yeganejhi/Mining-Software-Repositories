# src/merge_pipeline_data.py
import argparse
import os
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Merge final integrated data with Radon complexity metrics."
    )
    parser.add_argument(
        "--main-input",
        type=str,
        default="data/bugfix_dataset_final.csv",
        help="Path to the integrated bugfix dataset.",
    )
    parser.add_argument(
        "--complexity-input",
        type=str,
        default="data/bugfix_complexity.csv",
        help="Path to the Radon complexity metrics CSV.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/final_enriched_bugfixes.csv",
        help="Path to save the absolute final enriched dataset.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if not os.path.exists(args.main_input) or not os.path.exists(
        args.complexity_input
    ):
        print("❌ Error: One or both input files are missing. Check your path.")
        return

    print("📖 Loading datasets for final integration...")
    main_df = pd.read_csv(args.main_input)
    complexity_df = pd.read_csv(args.complexity_input)

    print("🧩 Injecting AST-based complexity metrics into the main dataset...")
    final_df = pd.merge(
        main_df, complexity_df, on="commit_hash", how="inner"
    )

    if "repo_name_x" in final_df.columns:
        final_df["repo_name"] = final_df["repo_name_x"]
        final_df = final_df.drop(columns=["repo_name_x", "repo_name_y"])

    final_df.to_csv(args.output, index=False)

    print("-" * 60)
    print(
        f"🚀 PIPELINE COMPLETE: Final Enriched Dataset Created with {len(final_df)} rows!"
    )
    print(f"📦 Absolute Final Output Saved to: {args.output}")
    print("-" * 60)


if __name__ == "__main__":
    main()