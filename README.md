# MSR-Pipeline: Automated Bug-Fix Mining and Metadata Enrichment

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)

An automated, robust Mining Software Repositories (MSR) pipeline designed to extract, clean, and enrich bug-fix commit data from remote GitHub repositories. This hybrid tool bridges the gap between raw Git process metrics (Code Churn) and source-code product metrics using Abstract Syntax Trees (AST).

---

## Why This Matters for Graduate Research

This pipeline directly addresses a critical gap in MSR empirical research: the computational trade-off between structural data richness (AST metrics) and storage efficiency (remote mining). By implementing a dynamic streaming architecture, this framework enables large-scale empirical software engineering studies without requiring terabytes of local repository storage. This makes comprehensive code-quality mining highly accessible and reproducible for researchers operating with limited hardware resources.

---

## Research Contributions

* **Methodological Novelty:** Introduces a hybrid pipeline that couples live, remote Git metadata streaming with AST-based complexity analysis without needing full local repository cloning.
* **Empirical Replicability:** Outlines a fully automated, end-to-end deterministic workflow, ensuring 100% reproducible data extraction for MSR benchmarks.
* **High Scalability:** Architected and evaluated against production-grade repositories containing extensive commit histories (e.g., PSF Requests, Flask), optimizing low-memory throughput.

---

## Technical Overview

In empirical software engineering, understanding structural decay and maintenance patterns requires a correlated analysis of process metrics (how code changes) and product metrics (how complex the code is). This project provides a multi-stage pipeline that automatically mines GitHub repositories, normalizes unstructured commit messages, tracks Code Churn (Lines Added/Deleted), and interfaces with AST analyzers to compute Cyclomatic Complexity scores.

```text
[Remote GitHub Repos] --> 1. collect_multiple_repos.py (Raw Mining)
                               |
                               v
                           2. extract_bugfix_commits.py (Regex Filter)
                               |
                               v
                           3. extract_clean_comments.py (UTC/Text Prep)
                               |
                               v
                           4. debug_lines_added_deleted.py (Hybrid Churn)
                               |
                               v
                           5. merge_bugfix_data.py (Integration Part I)
                               |
                               v
                           6. compute_complexity.py (AST Radon Engine)
                               |
                               v
                           7. merge_pipeline_data.py (Final Consolidation)
                               |
                               v
                    +---------+---------+
                    |                   |
                    v                   v
           8. eda_analysis.py    9. visualization.py
          (Statistical Models)  (Graphical Charts)
Key Challenges and SolutionsChallenge 1: Distributed Timezones and Data HeterogeneityContext: Commits extracted from global open-source contributors contain diverse, localized timestamp offsets.Solution: Implemented an aggressive datetime normalization layer using Pandas to force universal UTC alignment, resolving temporal misalignment in statistical tracking.Challenge 2: Network-Bound API Limits and Churn FailuresContext: Granular code churn analysis requires fetching live git diffs, which frequently causes network drops or API throttling.Solution: Configured lightweight dynamic streaming through PyDriller's internal generator layer, minimizing memory footprints and preventing connection timeouts.Challenge 3: Missing Local Trees for AST ParsersContext: Static analysis engines (e.g., Radon) strictly require a physical file system path to run abstract syntax parsing, which contradicts the remote cloning avoidance strategy.Solution: Architected a Truly Dynamic Hybrid Mode. When running online, the system dynamically fetches raw code snippets from GitHub’s API on the fly; when running locally, it performs a highly optimized tree search (os.walk) to map missing nested paths automatically.Sample Analytical OutputEmpirical Metrics SummaryThe pipeline extracts deep product and process metrics, exposing critical maintenance behavior (such as how complex files heavily restrict large-scale modifications):RepositoryBugfix Commits CheckedAvg Complexity (Radon CC)Max Complexity DiscoveredHigh-Complexity Functions (>5 CC)Key Insightspydriller43.9716.013High structural risk; bugs touch complex code.flask1Metadata OnlyMetadata Only0Non-functional configuration changes (setup.py).Key Statistical Discovery (Exploratory Data Analysis)Execution of the statistical layer (eda_analysis.py) uncovered a powerful empirical phenomenon:Statistical Correlation (Total Lines Changed vs. Max Complexity) = -0.79Interpretation: A strong negative correlation indicates that as a file's complexity nears critical levels (e.g., CC = 16), developers actively minimize the size of their bug-fixes. Out of structural fear, fixes become surgical, micro-level adjustments (e.g., modifying a single conditional block) rather than large-scale rewrites.Generated Insights & VisualizationsThe visualization layer produces high-resolution analytical plots saved automatically in the project directory:Distribution of Bug-Fix Change Size (plots/churn_vs_max_complexity.png)Tracks the size of historical patches alongside estimated probability density.(Placeholder Link: Replace with your actual repo link)Commit Distribution Across Targets (plots/high_complexity_totals.png)A standardized bar plot illustrating sample distribution density across repositories.(Placeholder Link: Replace with your actual repo link)Quick SetupPrerequisitesPython 3.8 or higherGitInstallationClone the repository and install the verified dependency manifest:Bashgit clone [https://github.com/yourusername/msr-pipeline.git](https://github.com/yourusername/msr-pipeline.git)
cd msr-pipeline
pip install -r requirements.txt
Note: The environment requires pandas, pydriller, radon, requests, matplotlib, and seaborn.Execution InstructionsThe pipeline can be executed in two different paradigms depending on your infrastructure requirements. Follow the corresponding recipe below:📡 Option A: Pure Remote / Online ModeIdeal when you want to avoid cloning repositories locally and stream everything directly from GitHub.Bash# Step 1: Mine metadata using full remote URLs
python src/collect_multiple_repos.py --repos [https://github.com/pallets/flask](https://github.com/pallets/flask) [https://github.com/ishepard/pydriller](https://github.com/ishepard/pydriller)

# Step 2: Filter bugfixes and clean text strings
python src/extract_bugfix_commits.py
python src/extract_clean_comments.py

# Step 3: Extract churn and calculate AST metrics via remote streaming
python src/debug_lines_added_deleted.py --mode online
python src/merge_bugfix_data.py
python src/compute_complexity.py --mode online

# Step 4: Final Consolidation & Analytics
python src/merge_pipeline_data.py
python src/eda_analysis.py
python src/visualization.py
💻 Option B: Local / Offline ModeIdeal when repositories are already cloned on your machine for ultra-fast local processing.Bash# Pre-requisite: Ensure your repositories are downloaded in a directory (e.g., F:/repos/)
# Step 1: Mine using short names
python src/collect_multiple_repos.py --repos flask pydriller

# Step 2: Filter bugfixes and clean text strings
python src/extract_bugfix_commits.py
python src/extract_clean_comments.py

# Step 3: Run local tree walks and extract churn from local paths
python src/debug_lines_added_deleted.py --mode local --repo-dir "F:/repos/"
python src/merge_bugfix_data.py
python src/compute_complexity.py --mode local --repo-dir "F:/repos/"

# Step 4: Final Consolidation & Analytics
python src/merge_pipeline_data.py
python src/eda_analysis.py
python src/visualization.py
Future DirectionsTool Integration: Integrate SonarQube APIs within the pipeline to extract deeper security vulnerabilities and code smell density metrics.Multi-Language Support: Expand the AST parsing sub-modules to interpret structural components of Java (via javalang) and JavaScript/TypeScript.Defect Prediction: Implement machine learning classification models (e.g., Random Forest) using the extracted process and product metrics to predict error-prone source components.Feedback and Academic InquiriesThis project is part of ongoing preparations for graduate research in software engineering. For academic inquiries, methodological reviews, or feature discussions, please open a technical issue or start a thread in the repository discussions tab.