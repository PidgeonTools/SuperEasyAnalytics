import argparse

# Process commit message.
parser = argparse.ArgumentParser()
parser.add_argument("--commit_message")
args = parser.parse_args()

# Extract the version from the commit message.
commit_message = args.commit_message
version = commit_message.split("#RELEASE")[1]
print(f"Version {version}")
