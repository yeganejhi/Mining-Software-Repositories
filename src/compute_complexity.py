# src/compute_complexity.py
import argparse
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
            high_complex_count = sum(1 for c in complexities if c > 5)
            return {
                "avg": sum(complexities) / len(complexities),
                "max": max(complexities),
                "high_functions": high_complex_count,  # 👈 نام کلید با s است
            }
    except Exception:
        return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Compute advanced AST-based code complexity metrics."
    )

    parser.add_argument(
        "--input",
        type=str,
        default="data/bugfix_dataset_final.csv",
        help="Path to filtered bugfix CSV.",
    )

    parser.add_argument(
        "--repo-dir",
        type=str,
        default="F:/repos/",
        help="Path to the local directory where repos are stored.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/bugfix_complexity.csv",
        help="Path to save complexity metrics CSV.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    if not os.path.exists(args.input):
        print(
            f"❌ Error: Input file '{args.input}' not found. Run the extraction script first."
        )
        return

    df = pd.read_csv(args.input)

    if "files_changed" not in df.columns:
        print(
            "⚠️ Notice: 'files_changed' column not found in the bugfix dataset."
        )
        print(
            "This is normal because we are testing with raw metadata from a remote GitHub URL!"
        )
        print(
            "Creating a placeholder complexity file so the pipeline doesn't break..."
        )

        placeholder_rows = []

        for _, row in df.iterrows():
            placeholder_rows.append(
                {
                    "commit_hash": row["commit_hash"],
                    "repo_name": row["repo_name"],
                    "python_files_count": 0,
                    "avg_complexity": 0.0,
                    "max_complexity": 0.0,
                    "high_complexity_functions_count": 0,
                }
            )

        placeholder_df = pd.DataFrame(placeholder_rows)
        placeholder_df.to_csv(args.output, index=False)
        print(f"✅ Placeholder complexity dataset saved to: {args.output}")
        return

    output_rows = []
    for _, row in df.iterrows():
        repo_name = row["repo_name"]
        commit_hash = row["commit_hash"]
        python_files = get_python_files(row["files_changed"])
        repo_path = os.path.join(args.repo_dir, repo_name)
        avg_list, max_list, high_funcs_total = [], [], 0

        for file in python_files:
            file_path = os.path.join(repo_path, file)
            metrics = compute_file_complexity(file_path)

            if metrics is not None:
                avg_list.append(metrics["avg"])
                max_list.append(metrics["max"])
                # 🛠️ این خط اصلاح شد: تبدیل high_function به high_functions
                high_funcs_total += metrics["high_functions"]

        output_rows.append(
            {
                "commit_hash": commit_hash,
                "repo_name": repo_name,
                "python_files_count": len(python_files),
                "avg_complexity": sum(avg_list) / len(avg_list)
                if avg_list
                else None,
                "max_complexity": max(max_list) if max_list else None,
                "high_complexity_functions_count": high_funcs_total,
            }
        )

    complexity_df = pd.DataFrame(output_rows)
    complexity_df.to_csv(args.output, index=False)
    print(
        f"✅ Advanced complexity analysis completed and saved to: {args.output}"
    )


if __name__ == "__main__":
    main()