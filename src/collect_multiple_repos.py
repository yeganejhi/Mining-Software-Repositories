# src/collect_multiple_repos.py
import argparse
import os
import shutil
import stat
import pandas as pd
from pydriller import Repository


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Extract commit history from local or remote Git repositories."
    )
    parser.add_argument(
        "--repos",
        nargs="+",
        required=True,
        help="List of repository paths or GitHub URLs.",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=50,
        help="Maximum number of commits per repository.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/multi_repo_commits.csv",
        help="Path to save output CSV.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_commits = []

    for repo_path in args.repos:
        repo_name = (
            repo_path.split("/")[-1].replace(".git", "")
            if "/" in repo_path
            else os.path.basename(repo_path)
        )
        print(
            f" Processing repository: {repo_name} (Max Commits: {args.max_commits})"
        )

        count = 0
        try:
            for commit in Repository(repo_path).traverse_commits():
                if count >= args.max_commits:
                    break

                commit_data = {
                    "repo_name": repo_name,
                    "repo_url": repo_path,
                    "commit_hash": commit.hash,
                    "message": commit.msg,
                    "date": commit.committer_date.isoformat(),
                    "author": commit.author.name,
                    "files_changed_count": len(commit.modified_files),
                }

                all_commits.append(commit_data)
                count += 1

        except Exception as e:
            print(f" Error processing repository {repo_path}: {e}")
            continue

    if not all_commits:
        print(" No commits collected.")
        return

    df = pd.DataFrame(all_commits)
    df.to_csv(args.output, index=False)

    print("\n Multi-repository dataset saved successfully!")
    print(f" Total commits collected: {len(df)} across {len(args.repos)} repos.")


if __name__ == "__main__":
    main()