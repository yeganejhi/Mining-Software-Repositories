import pandas as pd

def is_bugfix(message):
    if message is None :
        return False
    
    msg = message.lower()
    keywords =["fix","bug","error","issue","patch"]
    return any(key in msg for key in keywords)

# Load original commit dataset
df = pd.read_csv("data/multi_repo_commits.csv")

# Apply our function
df["is_bugfix"]=df["message"].apply(is_bugfix)

# Filter bug-fix commits
bugfix_df=df[df["is_bugfix"]==True]

bugfix_df.to_csv("data/bugfix_commits.csv", index=False)
print("Bug-fix dataset saved to data/bugfix_commits.csv")
print(f"Found {len(bugfix_df)} bug-fix commits")