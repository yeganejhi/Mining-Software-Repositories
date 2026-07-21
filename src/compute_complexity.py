# src/compute_complexity.py
import argparse
import os
import pandas as pd
import requests
import re
from radon.complexity import cc_visit
from git import Repo

def get_python_files(files_string):
    if pd.isna(files_string):
        return []
    files = str(files_string).split(";")
    py_files = [f.strip() for f in files if f.strip().endswith(".py")]
    return py_files

def fetch_online_source_code(repo_url, commit_hash, filename):
    try:
        if pd.isna(repo_url) or "github.com" not in str(repo_url):
            return None
            
        match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
        if match:
            owner = match.group(1)
            repo = match.group(2).replace(".git", "")
            
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit_hash}/{filename}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
    except Exception as e:
        print(f" Warning: Error fetching online source for {filename}: {e}")
    return None

def compute_code_complexity(code_text):
    try:
        results = cc_visit(code_text)
        if not results:
            return None

        complexities = [r.complexity for r in results]
        high_complex_count = sum(1 for c in complexities if c > 5)
        return {
            "avg": sum(complexities) / len(complexities),
            "max": max(complexities),
            "high_functions": high_complex_count, 
        }
    except Exception as e:
        print(f" Warning: Failed to compute complexity. Error: {e}")
        return None

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MSR Pipeline: Truly Dynamic Hybrid AST-based code complexity metrics."
    )
    parser.add_argument(
        "--input", type=str, default="data/bugfix_dataset_final.csv", help="Path to final bugfix CSV."
    )
    parser.add_argument(
        "--mode", type=str, default="local", choices=["local", "online"], help="Execution mode."
    )
    parser.add_argument(
        "--repo-dir", type=str, default="F:/repos/", help="Local repos path (for local mode)."
    )
    parser.add_argument(
        "--output", type=str, default="data/bugfix_complexity.csv", help="Path to save output."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    if not os.path.exists(args.input):
        print(f" Error: Input file '{args.input}' not found.")
        return

    df = pd.read_csv(args.input)
    output_rows = []

    print(f" Computing complexity in [{args.mode.upper()}] mode...")

    opened_repos = {}
    for _, row in df.iterrows():
        repo_name = row["repo_name"]
        commit_hash = row["commit_hash"]
        python_files = get_python_files(row.get("files_changed", ""))
        
        repo_url = row.get("repo_url", f"https://github.com/{repo_name}/{repo_name}")
        
        avg_list, max_list, high_funcs_total = [], [], 0

        for file in python_files:
            code_text = None

            if args.mode == "local":
                repo_path = os.path.join(args.repo_dir, repo_name)

                if repo_name not in opened_repos:
                    opened_repos[repo_name] = Repo(repo_path)
                repo = opened_repos[repo_name]
                
                git_file_path = file.replace("\\", "/")

                try:
                    code_text = repo.git.show(f"{commit_hash}:{git_file_path}")
                except Exception as e:
                    print(f" Warning: Could not read {git_file_path} at commit {commit_hash[:7]}. Error: {e}")
                    code_text = None

            else:
                code_text = fetch_online_source_code(repo_url, commit_hash, file)
            
            if code_text:
                metrics = compute_code_complexity(code_text)
                if metrics is not None:
                    avg_list.append(metrics["avg"])
                    max_list.append(metrics["max"])
                    high_funcs_total += metrics["high_functions"]

        output_rows.append(
            {
                "commit_hash": commit_hash,
                "repo_name": repo_name,
                "python_files_count": len(python_files),
                "avg_complexity": sum(avg_list) / len(avg_list) if avg_list else None,
                "max_complexity": max(max_list) if max_list else None,
                "high_complexity_functions_count": high_funcs_total,
            }
        )

    complexity_df = pd.DataFrame(output_rows)
    complexity_df.to_csv(args.output, index=False)
    print(f" Advanced complexity analysis completed! Saved to: {args.output}")

if __name__ == "__main__":
    main()