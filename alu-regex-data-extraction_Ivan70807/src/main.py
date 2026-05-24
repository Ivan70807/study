import re
import json
import os

# 1. Defining file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "input", "raw-text.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "sample-output.json")

# 2. Regex Patterns
# Email: Looks for characters, an @ symbol, characters, a dot, and an extension
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Credit Card: Looks for 4 groups of 4 digits separated by dashes or spaces
CREDIT_CARD_PATTERN = r'\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}'

# URL: Looks for http or https followed by :// and the website address characters
URL_PATTERN = r'https?://[a-zA-Z0-9./?=&-]+'

# Time: Looks for digits formatted as HH:MM or HH:MM AM/PM
TIME_PATTERN = r'\d{1,2}:\d{2}(?:\s?[APap][Mm])?'

# 3. Open and read txt file
print("Reading raw text input...")
file = open(INPUT_PATH, "r")
raw_text = file.read()
file.close()

# 4. Clean input
# Wipe out any dangerous HTML tags (like <script>) to prevent XSS attacks
clean_text = re.sub(r'<[^>]*>', '', raw_text)

# 5. Data extraction
# Find all occurrences of our patterns in the cleaned text
all_emails = re.findall(EMAIL_PATTERN, clean_text)
all_cards = re.findall(CREDIT_CARD_PATTERN, clean_text)
all_urls = re.findall(URL_PATTERN, clean_text)
all_times = re.findall(TIME_PATTERN, clean_text)

# 6. Structuring, validating and masking data
# Create final storage layout structure
output_data = {
    "urls": list(set(all_urls)),
    "times": list(set(all_times)),
    "credit_cards": [],
    "emails": {
        "alu_official": [],
        "alu_alumni": [],
        "alu_si": [],
        "general": []
    }
}

# Securely Process Credit Cards
for card in set(all_cards):
    # Security: Keep only the last 4 characters, mask the rest
    masked_card = "XXXX-XXXX-XXXX-" + card[-4:]
    output_data["credit_cards"].append(masked_card)

# Validate and Sort ALU Emails
for email in set(all_emails):
    # Keep first 2 characters, mask username, keep domain visible
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]
    masked_email = username[:2] + "xxx@" + domain

    # Sort by checking how the domain string ends
    if email.endswith("@alueducation.com"):
        output_data["emails"]["alu_official"].append(masked_email)
    elif email.endswith("@alumni.alueducation.com"):
        output_data["emails"]["alu_alumni"].append(masked_email)
    elif email.endswith("@si.alueducation.com"):
        output_data["emails"]["alu_si"].append(masked_email)
    else:
        output_data["emails"]["general"].append(masked_email)

# 7. Save the data to a JSON file
print("Writing structured results to JSON output...")
output_file = open(OUTPUT_PATH, "w")
json.dump(output_data, output_file, indent=4)
output_file.close()

print("Done! Open 'output/sample-output.json' to see the results.")