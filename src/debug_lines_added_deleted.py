from pydriller import Repository
import pandas as pd
import os

repos = ["F:/repos/pydriller", "F:/repos/flask"]
rows = []

bugfix_df = pd.read_csv("data/bugfix_commits.csv")
target_hashes = set(bugfix_df["commit_hash"])
for repo_path in repos:

    repo_name = os.path.basename(repo_path)
    print("Processing", repo_name)

    for commit in Repository(repo_path).traverse_commits():

        if commit.hash not in target_hashes:
            continue

        total_added = sum(m.added_lines for m in commit.modified_files)
        total_deleted = sum(m.deleted_lines for m in commit.modified_files)

        files = []
        for m in commit.modified_files:
            if m.new_path:
                files.append(m.new_path)

        files_changed = ";".join(files)
        rows.append({
            "repo_name": repo_name,
            "commit_hash": commit.hash,
            "lines_added": total_added,
            "lines_deleted": total_deleted,
            "files_changed": files_changed
        })

df = pd.DataFrame(rows)
df.to_csv("data/bugfix_with_lines.csv", index=False)
print("Done! Diff info extracted for", len(df), "bugfix commits")
