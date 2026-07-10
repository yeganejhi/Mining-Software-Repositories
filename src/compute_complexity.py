import argparse
import os
import pandas as pd
import requests
import re
from radon.complexity import cc_visit

def get_python_files(files_string):
    if pd.isna(files_string):
        return []
    files = str(files_string).split(";")
    py_files = [f.strip() for f in files if f.strip().endswith(".py")]
    return py_files

# پیدا کردن مسیر فایل روی هارد (مخصوص حالت لوکال)
def find_actual_file_path(repo_path, filename):
    for root, dirs, files in os.walk(repo_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# 💡 استخراج داینامیک سازمان و مخزن از روی لینک گیت‌هاب و دانلود سورس‌کد
def fetch_online_source_code(repo_url, commit_hash, filename):
    try:
        if pd.isna(repo_url) or "github.com" not in str(repo_url):
            return None
            
        # با ریجکس، نام سازمان و مخزن را از هر لینکی استخراج می‌کنیم
        # مثال: https://github.com/user/repo -> owner='user', repo='repo'
        match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
        if match:
            owner = match.group(1)
            repo = match.group(2).replace(".git", "")
            
            # ساخت آدرس فایل خام گیت‌هاب بدون هیچ هاردکدی
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit_hash}/{filename}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
    except Exception:
        pass
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
    except Exception:
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

    for _, row in df.iterrows():
        repo_name = row["repo_name"]
        commit_hash = row["commit_hash"]
        python_files = get_python_files(row.get("files_changed", ""))
        
        # پیدا کردن آدرس مخزن (اگر ستونش نبود یا خالی بود، یک فرض اولیه آنلاین می‌سازد)
        repo_url = row.get("repo_url", f"https://github.com/{repo_name}/{repo_name}")
        
        avg_list, max_list, high_funcs_total = [], [], 0

        for file in python_files:
            code_text = None

            if args.mode == "local":
                # خواندن آفلاین با جستجوی درختی در هارد
                repo_path = os.path.join(args.repo_dir, repo_name)
                actual_file_path = find_actual_file_path(repo_path, file)
                if actual_file_path and os.path.exists(actual_file_path):
                    try:
                        with open(actual_file_path, "r", encoding="utf-8") as f:
                            code_text = f.read()
                    except Exception:
                        pass
            else:
                # دانلود کاملاً داینامیک از گیت‌هاب بدون هاردکد
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