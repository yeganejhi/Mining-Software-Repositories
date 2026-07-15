import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="MSR Pipeline: Clean and format bug-fix commit messages.")
    parser.add_argument(
        "--input", type=str, default="data/bugfix_commits.csv", help="Path to raw bugfix commits CSV"
    )
    parser.add_argument(
        "--output", type=str, default="data/bugfix_clean.csv", help="Path to save clean commits CSV"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    df = pd.read_csv(args.input, na_values=[""])

    df["message"] = df["message"].str.strip()
    df.loc[df["message"] == "", "message"] = pd.NA

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    print("Missing values before drop:")
    print(df.isna().sum())

    df = df.dropna(subset=["commit_hash", "message", "date"])
    df = df.drop_duplicates(subset="commit_hash")

    df.to_csv(args.output, index=False)
    print(f"Saved: {len(df)} clean bugfix commits to {args.output}")

if __name__ == "__main__":
    main()