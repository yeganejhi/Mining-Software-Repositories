# src/debug_lines_added_deleted.py
from pydriller import Repository
import pandas as pd
import os
import argparse
import requests  

def parse_argument():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Extract file changes and line stats (diff) from GitHub dynamically."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/bugfix_commits.csv",
        help="path to filterd bugfix CSV"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/bugfix_with_lines.csv",
        help="Path to save the dataset with diff statistics.",
    )

    return parser.parse_args()
def fetch_online_diff_stats(repo_url, commit_hash):
    try:
        repo = Repository(repo_url, single=commit_hash)
        # 🛠️ این خط اصلاح شد: تبدیل repo.traverse.commits به repo.traverse_commits
        for commit in repo.traverse_commits():
            py_files = []
            insertions = 0
            deletions = 0

            for modified_file in commit.modified_files:
                filename = modified_file.filename

                if filename.endswith(".py"):
                    py_files.append(filename)

                insertions += modified_file.added_lines
                deletions += modified_file.deleted_lines

            files_string = ";".join(py_files) if py_files else None

            return {
                "files_changed": files_string,
                "lines_added": insertions,
                "lines_deleted": deletions,
            }
    except Exception:
        return {"files_changed": None, "lines_added": 0, "lines_deleted": 0}
    
def main():
    args = parse_argument()

    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found. Run the extraction script first.")
        return
    
    print(f"📖 Loading filtered bug-fix commits from: {args.input}")
    df = pd.read_csv(args.input)

    if "repo_url" not in df.columns:
        df["repo_url"] = "https://github.com/psf/requests"

    print("🌐 Connecting to GitHub dynamically to fetch diff statistics...")

    files_changed_list = []
    lines_added_list = []
    lines_deleted_list = []

    for _,row in df.iterrows():
        url = row["repo_url"]
        commit_hash = row["commit_hash"]

        print(f"🔗 Fetching stats for commit: {commit_hash[:7]}...")

        stats = fetch_online_diff_stats(url,commit_hash)

        files_changed_list.append(stats["files_changed"])
        lines_added_list.append(stats["lines_added"])
        lines_deleted_list.append(stats["lines_deleted"])

    df["files_changed"] = files_changed_list
    df["lines_added"] = lines_added_list
    df["lines_deleted"] = lines_deleted_list

    df.to_csv(args.output, index=False)
    print(f"✅ Online diff extraction completed! Dataset saved to: {args.output}")
if __name__ == "__main__":
    main()

