import os
import pandas as pd
from radon.complexity import cc_visit


# extract python files
def get_python_files(files_string):
    if pd.isna(files_string):
        return []
    files = str(files_string).split(";")
    py_files = [f.strip() for f in files if f.strip().endswith(".py")]
    return py_files


# compute avg complexity of one file
def compute_file_complexity(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            results = cc_visit(code)

            if not results:
                return None

            complexities = [r.complexity for r in results]
            return sum(complexities) / len(complexities)

    except Exception:
        return None


df = pd.read_csv("data/bugfix_with_lines.csv")

output_rows = []

print(df["files_changed"].head())
print(get_python_files(df.iloc[0]["files_changed"]))


for _, row in df.iterrows():

    repo_name = row["repo_name"]
    commit_hash = row["commit_hash"]
    files_changed = row["files_changed"]

    python_files = get_python_files(files_changed)

    repo_path = f"F:/repos/{repo_name}"

    complexities = []

    for file in python_files:

        file_path = os.path.join(repo_path, file)

        c = compute_file_complexity(file_path)

        if c is not None:
            complexities.append(c)

    avg_complexity = None
    if complexities:
        avg_complexity = sum(complexities) / len(complexities)

    output_rows.append({
        "commit_hash": commit_hash,
        "repo_name": repo_name,
        "python_files_count": len(python_files),
        "avg_complexity": avg_complexity
    })


complexity_df = pd.DataFrame(output_rows)

complexity_df.to_csv("data/bugfix_complexity.csv", index=False)

print("complexity analysis completed.")
print(complexity_df.head())
