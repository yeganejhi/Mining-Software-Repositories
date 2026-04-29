import pandas as pd

df = pd.read_csv("data/bugfix_dataset_final.csv")

print("Mean lines added:", df["lines_added"].mean())
print("Median lines added:", df["lines_added"].median())
print("Mean lines deleted:", df["lines_deleted"].mean())
print("Median lines deleted:", df["lines_deleted"].median())

print("\nTop 10 biggest bug-fix commits (by lines_added):")
print(df.sort_values("lines_added", ascending=False).head(10))

print("\nBug-fix count per repository:")
print(df["repo_name"].value_counts())

print("\nAverage lines_added per repo:")
print(df.groupby("repo_name")["lines_added"].mean().sort_values(ascending=False))

print("\nAverage lines_deleted per repo:")
print(df.groupby("repo_name")["lines_deleted"].mean().sort_values(ascending=False))