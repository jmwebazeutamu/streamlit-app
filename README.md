# Input Validation Teaching App (Streamlit)

Single-page Streamlit app for Software Design classes.

It demonstrates unsafe vs validated handling for common input-validation cases:
- type checks
- range checks
- format checks
- allowlist/denylist checks
- SQL injection-safe query pattern
- ZIP regex checks
- file upload validation
- semantic (cross-field) validation

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Notes

- Entry point: `app.py`
- No database or authentication required
