
import os
from os import path as p

# Create a README, if it doesn't exist already.
if not "README.md" in os.listdir():
  exit()
  
# Get the content of the README file.
with open("README.md", "r") as f:
  text = f.read()
content = text.split("<!-- CHANGELOG -->")[1]

# Count, which types of features have been added and how often.
data = {
    "Features": len(content.split("- Feature")) - 1,
    "Improvements": len(content.split("- Improvement")) - 1,
    "Fixes": len(content.split("- Fix")) - 1,
}

output = "This release comes with "
for key in data.keys():
    # Check, if there even are features of the current feature type.
    if data[key] > 0:
        feature_type = key
        if data[key] == 1:
            # Get the singular form of the feature type.
            feature_type = key[:-1]

            # Special case: Fixes are called "Fix" in singular.
            if feature_type == "Fixe":
                feature_type = "Fix"

        # Compose the output.
        output += f"{data[key]} {feature_type}, "
with open("../release_description.txt", "w+") as f:
  f.write(f"{output[:-2]}:{content}")
