import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/bugfix_dataset_final.csv")
df["lines_changed"] = df["lines_added"]+ df["lines_deleted"]
print(df[["lines_added", "lines_deleted", "lines_changed"]])

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="lines_changed",
    bins=10,
    kde=True
)

plt.title("Distribution of Bug-Fix Change Size")
plt.xlabel("Lines Changed (Added + Deleted)")
plt.ylabel("Number of Commits")

plt.show()

repo_counts = df["repo_name"].value_counts().reset_index()
repo_counts.columns=["repo_name","bugfix_count"]
print(repo_counts)

plt.figure(figsize=(7,5))
sns.barplot(
    data=repo_counts,
    x="repo_name",
    y="bugfix_count"
)

plt.title("Number of Bug-Fix Commits per Repository")
plt.xlabel("Repository")
plt.ylabel("Bug-Fix Commit Count")

plt.show()

plt.figure(figsize=(7,5))

sns.boxplot(
    data=df,
    y="lines_changed"
)
plt.title("Boxplot of Bug-Fix Change Size")
plt.ylabel("Lines Changed")
# plt.ylim(0, 200)


plt.show()


