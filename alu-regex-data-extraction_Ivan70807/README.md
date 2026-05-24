# Data Extraction & Secure Validation Utility

This project extracts structured data from messy real world text blocks, sanitizes unsafe content, and organizes data into dynamic JSON outputs.
It fulfills all junior developer requirements for defensive coding and validation.

The src/main.py script executes sequentially across these core blocks:

1. Path Definitions: The script uses the `os` module to dynamically resolve the project's root folder relative to `main.py`,
which works in different operating systems and avoids crashing.

2. Regex Compilation: Uses targeted patterns (re) to extract four critical formats: URLs, Times (12h/24h), 16-digit Credit Cards, and Domain Emails.

3. Defensive Pre-processing: Runs re.sub(r'<[^>]*>', '', text) to instantly strip out malicious HTML/Script injections 
(mitigating XSS vulnerabilities before storage).

4. PII Masking Loop: Loops through sensitive parameters to mask them. Credit cards show only the final 4 digits (XXXX-XXXX-XXXX-1234),
and email prefixes are split and minimized to preserve security.

5. ALU Domain Routing: Tracks string suffixes using .endswith() to automatically filter emails into their exact corporate tiers 
(@alueducation.com, @alumni.alueducation.com, or @si.alueducation.com).

6. Data Deduplication: Wraps raw findings into a Python set() array to discard repeating items instantly.

7. JSON Export: Serializes the organized layout into a clean, human-readable file using json.dump(..., indent=4).

# Running Instructions
Python 3.x installed locally.

A) Save your messy input logs inside input/raw-text.txt.

B) Open your terminal at the root directory (alu-regex-data-extraction_Ivan70807/).

C) Run the following command:
   python src/main.py

D) Verify the structured payload results inside output/sample-output.json.