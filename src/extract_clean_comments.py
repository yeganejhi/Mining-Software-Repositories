import pandas as pd

df = pd.read_csv("data/bugfix_commits.csv", na_values=[""])

df["message"] = df["message"].str.strip()
df.loc[df["message"] == "", "message"] = pd.NA

df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

print(df.isna().sum())

df = df.dropna(subset=["commit_hash", "message", "date"])

df = df.drop_duplicates(subset="commit_hash")

df.to_csv("data/bugfix_clean.csv", index=False)
print("Saved:", len(df), "clean bugfix commits")
