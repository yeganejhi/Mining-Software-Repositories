from pydriller import Repository
import pandas as pd
import os

repos=["F:/repos/pydriller",
    "F:/repos/flask"
]

all_commits=[]

for repo_path in repos:

    repo_name = os.path.basename(repo_path)
    print(f"Processing repository: {repo_name}")

    count = 0

    for commit in Repository(repo_path).traverse_commits():

        if count >= 50:
            break

        commit_data = {
            "repo_name": repo_name,
            "commit_hash": commit.hash,
            "message": commit.msg,
            "date": commit.committer_date,
            "author": commit.author.name,
            "files_changed_count": commit.files  
        }

        all_commits.append(commit_data)
        count += 1
df=pd.DataFrame(all_commits)
df.to_csv("data/multi_repo_commits.csv", index=False)
print("Multi-repository dataset saved!")
print(f"Total commits collected: {len(df)}")