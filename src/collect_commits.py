from pydriller import Repository

repo_path = "F:/projects/msr-bugfix-analysis"   

count = 0

for commit in Repository(repo_path).traverse_commits():
    print("----- COMMIT -----")
    print("Hash:", commit.hash)
    print("Message:", commit.msg)
    print("Author:", commit.author.name)
    print("Date:", commit.author_date)
    print("Modified files:", len(commit.modified_files))
    
    count += 1
    if count == 10:
        break
