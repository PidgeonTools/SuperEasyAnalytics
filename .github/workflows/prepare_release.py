import argparse

import os
from os import path as p

# Process commit message.
parser = argparse.ArgumentParser()
parser.add_argument("--commit_message")
parser.add_argument("--repo_url")
parser.add_argument("--include_issue_notice")
args = parser.parse_args()

# Extract the version from the commit message.
commit_message = args.commit_message
version_raw = commit_message.split("#RELEASE")[1]
version = version_raw.replace(".", "_")
print(version)

# Create a README, if it doesn't exist already.
if not "README.md" in os.listdir():
    with open("README.md", "w+") as f:
        f.write("<!-- CHANGELOG -->\n\n<!-- CHANGELOG -->")
    exit()

# Get the content of the README file.
with open("README.md", "r") as f:
    text = f.read()
text = text.split("<!-- CHANGELOG -->")

# Generate an issue notice text, if configured.
issue_notice_text = ""
if args.include_issue_notice.lower() == "true":
    issue_url = f"https://github.com/{args.repo_url}/issues/new/choose"
    issue_notice_text = f"\nWe've just hit another update. No features are planned so far. [Change this!]({issue_url})"

# Update the README file.
with open("README.md", "w+") as f:
    f.write(
        f"{text[0]}{issue_notice_text}\n<!-- CHANGELOG -->\n\n<!-- CHANGELOG -->{text[2]}")

# Compose the changelog text.
changelog_text = f"""## Version {version_raw}
{text[1]}"""

prev_text = ""
if "CHANGELOG.md" in os.listdir():
    with open("CHANGELOG.md", "r") as f:
        prev_text = f.read()

final_text = f"""{changelog_text}

{prev_text}
"""

with open("CHANGELOG.md", "w+") as f:
    f.write(final_text)
