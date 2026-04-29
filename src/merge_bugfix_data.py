import pandas as pd

clean_df = pd.read_csv("data/bugfix_clean.csv")
lines_df = pd.read_csv("data/bugfix_with_lines.csv")

df = pd.merge(
    clean_df,
    lines_df,
    on=["repo_name", "commit_hash"],
    how="inner"
)

df.to_csv("data/bugfix_dataset_final.csv", index=False)

print("Final dataset created!")
print("Total rows:", len(df))
print("Columns:", df.columns)
