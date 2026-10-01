## What
Added a complete quick-start example so users can run the scraper in 2 minutes:
- Updated README.md with clear installation and usage steps.
- Provided .env.example with required variables (FIRECRAWL_API_KEY, TARGET_URL, OUTPUT_CSV).
- Added data/sample.csv showing expected output format (id,name,price,url).

## Why
The repository lacked a ready-to-run example, making it hard for potential users/customers to see the value quickly.
This addresses issue #59 (update .env.example) and improves overall usability.

## How
- Edited README.md to include a 2-minute quick start guide.
- Ensured .env.example contains all necessary variables.
- Created a representative sample CSV in data/sample.csv.
- Ran the existing test suite to confirm no regressions.

## Testing
- Ran `python3 -m pytest test_scraper.py -v` (see evidencia_ejecucion.txt).
- Verified the scraper imports and runs without syntax errors.
- Confirmed the sample CSV matches the expected columns.

## Evidence
Test output saved in evidencia_ejecucion.txt.
