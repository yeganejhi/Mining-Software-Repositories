# src/merge_bugfix_data.py
import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="MSR Pipeline: Merge clean commits with line change statistics.")
    parser.add_argument(
        "--clean-input", type=str, default="data/bugfix_clean.csv", help="Path to clean bugfix CSV"
    )
    parser.add_argument(
        "--lines-input", type=str, default="data/bugfix_with_lines.csv", help="Path to lines statistics CSV"
    )
    parser.add_argument(
        "--output", type=str, default="data/bugfix_dataset_final.csv", help="Path to save final dataset"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    clean_df = pd.read_csv(args.clean_input)
    lines_df = pd.read_csv(args.lines_input)

    df = pd.merge(
        clean_df,
        lines_df, 
        on=["repo_name", "commit_hash"],
        how="inner"
    )
    
    df = df.rename(columns={
        "repo_url_x": "repo_url",
        "message_x": "message",
        "date_x": "date",
        "author_x": "author",
        "files_changed_count_x": "files_changed_count",
    })

    df = df.drop(columns=[
        "repo_url_y",
        "message_y",
        "date_y",
        "author_y",
        "files_changed_count_y",
    ])

    df.to_csv(args.output, index=False)

    print("Final dataset created successfully!")
    print(f"Total rows: {len(df)}")
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()