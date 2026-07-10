# src/extract_bugfix_commits.py
import pandas as pd
import argparse
import os
import re
def is_bugfix(message):
    if pd.isna(message) :
        return False
    msg = str(message).lower()
    positive_pattern = r"\b(fix|bug|error|issue|patch|defect|crash|resolve)\b"

    negative_pattern = (
        r"\b(typo|docs|readme|documentation|release|version|merge branch)\b"
    )
    if re.search(positive_pattern,msg):
        if re.search(negative_pattern,msg):
            return False
        return True
    return False
def parse_arguments():
    parser = argparse.ArgumentParser(description="MSR Pipeline: Filter bug-fixing commits using advanced text-heuristics.")
    parser.add_argument(
        "--input",
        type=str,
        default="data/multi_repo_commits.csv",
        help="Path to the raw commits CSV file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/bugfix_commits.csv",
        help="Path to save the filtered bug-fix commits CSV.",
    )
    return parser.parse_args()
    

def main():
    args = parse_arguments()
    if not os.path.exists(args.input):
        print(f" Error: Input file '{args.input}' does not exist.")
        return
    
    print(f" Loading dataset from: {args.input}")
    df = pd.read_csv(args.input)
    print(" Applying advanced bug-fix heuristics...")
    df["is_bugfix"] = df["message"].apply(is_bugfix)

    bugfix_df = df[df["is_bugfix"]==True].copy()
    bugfix_df = bugfix_df.drop(columns=["is_bugfix"])

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    bugfix_df.to_csv(args.output, index=False)
    print(f" Bug-fix dataset saved! Found {len(bugfix_df)} commits.")
if __name__ == "__main__":
    main()