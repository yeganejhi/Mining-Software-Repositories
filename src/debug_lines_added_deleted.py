# src/debug_lines_added_deleted.py
from pydriller import Repository
import pandas as pd
import os
import argparse

def parse_argument():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Robust Hybrid Diff Statistics Extractor."
    )
    parser.add_argument(
        "--input", type=str, default="data/bugfix_commits.csv", help="path to filtered bugfix CSV"
    )
    parser.add_argument(
        "--output", type=str, default="data/bugfix_with_lines.csv", help="Path to save output"
    )
    parser.add_argument(
        "--mode", type=str, default="local", choices=["local", "online"], 
        help="Choose 'local' to use your physical hard drive or 'online' to use URLs."
    )
    parser.add_argument(
        "--repo-dir", type=str, default="F:/repos", help="Base directory for local mode"
    )
    return parser.parse_args()

def fetch_diff_stats(repo_path, commit_hash):
    try:
        repo = Repository(repo_path, single=commit_hash)

        for commit in repo.traverse_commits():
            py_files = []
            insertions = 0
            deletions = 0

            for modified_file in commit.modified_files:

                file_path = modified_file.new_path or modified_file.old_path

                if file_path and file_path.endswith(".py"):
                    py_files.append(file_path)

                insertions += modified_file.added_lines
                deletions += modified_file.deleted_lines

            files_string = ";".join(py_files) if py_files else None

            return {
                "files_changed": files_string,
                "lines_added": insertions,
                "lines_deleted": deletions,
            }

    except Exception as e:
        print(f"Error processing commit {commit_hash}: {e}")
        return {
            "files_changed": None,
            "lines_added": 0,
            "lines_deleted": 0,
        }
    
def main():
    args = parse_argument()
    if not os.path.exists(args.input):
        print(f" Error: Input file '{args.input}' not found.")
        return
    
    df = pd.read_csv(args.input)

    files_changed_list = []
    lines_added_list = []
    lines_deleted_list = []

    print(f" Running pipeline in [{args.mode.upper()}] mode...")

    for _, row in df.iterrows():
        commit_hash = row["commit_hash"]
        repo_name = row["repo_name"]

        if args.mode == "local":
            path_to_open = os.path.join(args.repo_dir, repo_name)
        else:
            if "repo_url" in df.columns and pd.notna(row["repo_url"]):
                path_to_open = row["repo_url"]
            else:
                path_to_open = repo_name

        print(f" Target Path -> {path_to_open} (Commit: {commit_hash[:7]})")
        stats = fetch_diff_stats(path_to_open, commit_hash)

        files_changed_list.append(stats["files_changed"])
        lines_added_list.append(stats["lines_added"])
        lines_deleted_list.append(stats["lines_deleted"])

    df["files_changed"] = files_changed_list
    df["lines_added"] = lines_added_list
    df["lines_deleted"] = lines_deleted_list

    df.to_csv(args.output, index=False)
    print(f" Success! Dataset saved to: {args.output}")

if __name__ == "__main__":
    main()