# Input Validation Teaching App (Streamlit)

This app demonstrates why input validation is essential in software design.
It shows side-by-side behavior for unsafe and validated flows.

## Covered examples

- Type checks
- Range checks
- Format checks
- Allowlist role checks
- SQL injection risk
- Allow-listing vs deny-listing strategies
- Regex validation for U.S. ZIP Codes (`12345` or `12345-6789`)
- File upload validation (type, size, and basic content checks)
- Semantic validation (cross-field business rules on dates)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Suggested class activity

1. Enter malformed or malicious values in each tab.
2. Run unsafe behavior first and observe failures/risks.
3. Run the validated behavior and compare outcomes.
4. Discuss which validation strategy (type/range/format/allowlist/semantic) blocked the issue.
