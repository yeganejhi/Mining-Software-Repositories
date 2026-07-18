import argparse
import subprocess
import sys

def run_step(command):
    print("\n" + "=" * 60)
    print(f"Running: {command}")
    print("=" * 60)
    result = subprocess.run(
        command,
        shell=True
    )
    if result.returncode != 0:
        print(f"Failed: {command}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="MSR Bug-Fix Analysis Pipeline Runner"
    )

    parser.add_argument(
        "--mode",
        choices=["local", "online"],
        default="local"
    )

    parser.add_argument(
        "--repo-dir",
        default="F:/repos/",
        help="Local repository directory"
    )

    args = parser.parse_args()


    steps = [
        "python src/extract_bugfix_commits.py",
        "python src/extract_clean_comments.py",
        f"python src/debug_line_added_deleted.py "
        f"--mode {args.mode} "
        f'--repo-dir "{args.repo_dir}"',
        "python src/merge_bugfix_data.py",
        f"python src/compute_complexity.py "
        f"--mode {args.mode} "
        f'--repo-dir "{args.repo_dir}"',

        "python src/merge_pipeline_data.py",
        "python src/eda_analysis.py",
        "python src/visualization.py"

    ]


    print("""
========================================
 MSR Bug-Fix Analysis Pipeline
========================================
""")
    for step in steps:
        run_step(step)
    print("""
========================================
 Pipeline Completed Successfully!
========================================
""")
if __name__ == "__main__":
    main()