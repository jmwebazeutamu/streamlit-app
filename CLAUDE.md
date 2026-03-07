# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

## Architecture

This is a multipage Streamlit app for the ITP100 course.

- **`app.py`** — Entry point. Registers all pages via `st.navigation()` and runs the navigator.
- **`module_pages/`** — Each file is a self-contained Streamlit page:
  - `home.py` — Landing page with navigation instructions
  - `module7_input_validation.py` — Input validation demo and class assignment form
  - `module8_arrays.py` — Interactive arrays practice (Gaddis Chapter 8)
  - `module8_arrays_react.py` — Arrays practice with React-style activities
  - `chatbot_demo.py` — Chatbot demo page
- **`static/`** — Static HTML assets (e.g. standalone validation exercise)

To add a new page, create a file in `module_pages/` and register it in the `pages` list in `app.py`.
