import os
import re
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Why Input Validation Matters", page_icon="✅", layout="wide")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def unsafe_checkout(price_text: str, qty_text: str) -> float:
    return float(price_text) * int(qty_text)


def safe_checkout(price_text: str, qty_text: str) -> float:
    if not re.fullmatch(r"\d+(\.\d{1,2})?", price_text.strip()):
        raise ValueError("Price must be a positive number with up to 2 decimals.")
    if not re.fullmatch(r"\d+", qty_text.strip()):
        raise ValueError("Quantity must be a whole number.")

    price = float(price_text)
    qty = int(qty_text)

    if price <= 0:
        raise ValueError("Price must be greater than 0.")
    if qty < 1 or qty > 1000:
        raise ValueError("Quantity must be between 1 and 1000.")

    return price * qty


def unsafe_event_year(year_text: str) -> int:
    return datetime.now().year - int(year_text)


def safe_event_year(year_text: str) -> int:
    if not re.fullmatch(r"\d{4}", year_text.strip()):
        raise ValueError("Year must be exactly 4 digits.")

    year = int(year_text)
    current = datetime.now().year
    if year < 1900 or year > current:
        raise ValueError(f"Year must be between 1900 and {current}.")

    return current - year


def unsafe_email_accept(email: str) -> str:
    return f"Stored email as entered: {email}"


def safe_email_accept(email: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email.strip()):
        raise ValueError("Email format is invalid.")
    return f"Stored normalized email: {email.strip().lower()}"


def unsafe_role_assignment(role: str) -> str:
    return f"Granted role: {role}"


def safe_role_assignment(role: str) -> str:
    allowed_roles = {"student", "teacher", "assistant"}
    cleaned = role.strip().lower()
    if cleaned not in allowed_roles:
        raise ValueError(f"Role must be one of: {', '.join(sorted(allowed_roles))}.")
    return f"Granted role: {cleaned}"


def unsafe_login_query(username: str, password: str) -> str:
    return (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "';"
    )


def safe_login_query(username: str, password: str) -> tuple[str, tuple[str, str]]:
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username.strip()):
        raise ValueError("Username must be 3-30 chars: letters, numbers, underscore.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    return "SELECT * FROM users WHERE username = ? AND password = ?;", (username.strip(), password)


def denylist_only_username(username: str) -> str:
    blocked = {"admin", "root", "superuser"}
    cleaned = username.strip().lower()
    if cleaned in blocked:
        raise ValueError("Username blocked by deny-list.")
    return f"Accepted username: {username}"


def allowlist_username(username: str) -> str:
    cleaned = username.strip()
    blocked = {"admin", "root", "superuser"}
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,19}", cleaned):
        raise ValueError("Must start with a letter and be 3-20 chars: letters, numbers, underscore.")
    if cleaned.lower() in blocked:
        raise ValueError("Reserved username not allowed.")
    return f"Accepted username: {cleaned}"


def validate_us_zip(zip_code: str) -> str:
    cleaned = zip_code.strip()
    if not re.fullmatch(r"\d{5}(-\d{4})?", cleaned):
        raise ValueError("Use 5 digits (12345) or ZIP+4 (12345-6789).")
    return cleaned


def validate_upload(file_name: str, file_bytes: bytes) -> str:
    allowed_ext = {".csv", ".txt"}
    ext = os.path.splitext(file_name.lower())[1]
    max_size = 1 * 1024 * 1024

    if ext not in allowed_ext:
        raise ValueError("Only .csv and .txt files are allowed.")
    if len(file_bytes) > max_size:
        raise ValueError("File too large. Max size is 1 MB.")

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File must be UTF-8 text.") from exc

    if ext == ".csv":
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if "," not in first_line:
            raise ValueError("CSV appears invalid: missing comma-separated header.")

    return f"Validated upload: {file_name} ({len(file_bytes)} bytes)"


def unsafe_trip_dates(booking_date: str, travel_date: str) -> int:
    booking = datetime.strptime(booking_date, "%Y-%m-%d")
    travel = datetime.strptime(travel_date, "%Y-%m-%d")
    return (travel - booking).days


def safe_trip_dates(booking_date: str, travel_date: str) -> int:
    booking = datetime.strptime(booking_date, "%Y-%m-%d")
    travel = datetime.strptime(travel_date, "%Y-%m-%d")

    if travel < booking:
        raise ValueError("Travel date cannot be before booking date.")
    if (travel - booking).days > 365:
        raise ValueError("Travel date is too far in the future (max 365 days).")

    return (travel - booking).days


def validate_rps_choice(choice: str) -> str:
    normalized = choice.strip().lower()
    mapping = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}
    if normalized not in mapping:
        raise ValueError("Enter only Rock, Paper, or Scissors.")
    return mapping[normalized]


def validate_ticket_count(raw_value: str, section_name: str, capacity: int) -> int:
    cleaned = raw_value.strip()
    if not re.fullmatch(r"\d+", cleaned):
        raise ValueError(f"Section {section_name}: enter a whole number 0 to {capacity}.")
    count = int(cleaned)
    if count < 0 or count > capacity:
        raise ValueError(
            f"Section {section_name}: tickets sold must be between 0 and {capacity}."
        )
    return count


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("Input Validation Demo for Software Design")
st.write(
    "This app shows what happens when systems trust input too much, then shows the validated version."
)

st.info(
    "Teaching goal: help students connect validation to reliability, security, and data quality."
)

with st.expander("Quick Guide: How to Use This Tool"):
    st.markdown(
        """
1. Pick any tab (example topic) at the top.
2. Enter test input values.
3. Run the **unsafe** version first to see the risk.
4. Run the **validated** version to compare behavior.
5. Read the message shown (`success`, `warning`, or `error`) and explain what rule was applied.
"""
    )


tabs = st.tabs(
    [
        "Type Checks",
        "Range Checks",
        "Format Checks",
        "Allowlist Checks",
        "Injection Risk",
        "Allow vs Deny List",
        "Regex: US ZIP",
        "File Upload Validation",
        "Semantic Validation",
        "RPS Validation",
        "Theater Revenue",
    ]
)

with tabs[0]:
    st.subheader("1) Type Validation")
    st.caption("Scenario: checkout total from price and quantity")

    c1, c2 = st.columns(2)
    with c1:
        price = st.text_input("Price", value="12.50", key="type_price")
    with c2:
        qty = st.text_input("Quantity", value="2", key="type_qty")

    a, b = st.columns(2)

    with a:
        st.markdown("**No validation**")
        if st.button("Run unsafe checkout", key="run_unsafe_type"):
            try:
                total = unsafe_checkout(price, qty)
                st.success(f"Total: ${total:.2f}")
            except Exception as exc:
                st.error(f"App crashed: {exc}")

    with b:
        st.markdown("**With validation**")
        if st.button("Run safe checkout", key="run_safe_type"):
            try:
                total = safe_checkout(price, qty)
                st.success(f"Total: ${total:.2f}")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[1]:
    st.subheader("2) Range Validation")
    st.caption("Scenario: years since an event")

    event_year = st.text_input("Event year", value="2020", key="range_year")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation**")
        if st.button("Run unsafe year calc", key="run_unsafe_range"):
            try:
                years = unsafe_event_year(event_year)
                st.success(f"Years since event: {years}")
            except Exception as exc:
                st.error(f"App crashed: {exc}")

    with b:
        st.markdown("**With validation**")
        if st.button("Run safe year calc", key="run_safe_range"):
            try:
                years = safe_event_year(event_year)
                st.success(f"Years since event: {years}")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[2]:
    st.subheader("3) Format Validation")
    st.caption("Scenario: storing email addresses")

    email = st.text_input("Email", value="student@school.edu", key="format_email")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation**")
        if st.button("Run unsafe email", key="run_unsafe_format"):
            st.success(unsafe_email_accept(email))

    with b:
        st.markdown("**With validation**")
        if st.button("Run safe email", key="run_safe_format"):
            try:
                st.success(safe_email_accept(email))
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[3]:
    st.subheader("4) Allowlist Validation")
    st.caption("Scenario: assigning application roles")

    role = st.text_input("Requested role", value="student", key="allow_role")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation**")
        if st.button("Run unsafe role assignment", key="run_unsafe_role"):
            st.success(unsafe_role_assignment(role))
            st.error("Risk: attacker can request 'admin' or unknown privileged roles.")

    with b:
        st.markdown("**With validation**")
        if st.button("Run safe role assignment", key="run_safe_role"):
            try:
                st.success(safe_role_assignment(role))
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[4]:
    st.subheader("5) Injection Risk")
    st.caption("Scenario: login query construction")

    username = st.text_input("Username", value="alice", key="inj_user")
    password = st.text_input("Password", value="mypassword", key="inj_pass")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation / string concatenation**")
        if st.button("Build unsafe SQL", key="run_unsafe_sql"):
            query = unsafe_login_query(username, password)
            st.code(query, language="sql")
            st.error(
                "Risk: malicious input like `' OR '1'='1` can alter the query logic."
            )

    with b:
        st.markdown("**With validation + parameterized query**")
        if st.button("Build safe SQL", key="run_safe_sql"):
            try:
                query, params = safe_login_query(username, password)
                st.code(query, language="sql")
                st.write(f"Parameters: {params}")
                st.success("Input validated and SQL separated from data.")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[5]:
    st.subheader("6) Allow-listing vs Deny-listing")
    st.caption("Scenario: username policy")

    username_policy = st.text_input(
        "Username candidate", value="admin1", key="policy_username"
    )
    st.write("Try values like `admin`, `admin1`, `root_user`, `john-doe`, `_alice`.")

    a, b = st.columns(2)
    with a:
        st.markdown("**Deny-list only**")
        if st.button("Run deny-list check", key="run_denylist"):
            try:
                st.success(denylist_only_username(username_policy))
                st.error("Risk: variants like `admin1` pass because they are not exactly blocked.")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

    with b:
        st.markdown("**Allow-list + reserved-word deny-list**")
        if st.button("Run allow-list check", key="run_allowlist"):
            try:
                st.success(allowlist_username(username_policy))
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[6]:
    st.subheader("7) Regular Expressions: Validate U.S. ZIP Code")
    st.caption("Accepted formats: 12345 or 12345-6789")

    zip_code = st.text_input("ZIP code", value="02139", key="zip_code")
    if st.button("Validate ZIP", key="run_zip_validation"):
        try:
            cleaned = validate_us_zip(zip_code)
            st.success(f"Valid ZIP: {cleaned}")
        except Exception as exc:
            st.warning(f"Invalid ZIP: {exc}")

with tabs[7]:
    st.subheader("8) File Upload Validation")
    st.caption("Scenario: accepting homework submissions")

    uploaded = st.file_uploader("Upload a file", key="upload_demo")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation**")
        if st.button("Accept file unsafely", key="run_unsafe_upload"):
            if uploaded is None:
                st.warning("Please upload a file first.")
            else:
                st.success(f"Accepted file: {uploaded.name}")
                st.error("Risk: executable, oversized, or malformed files can be accepted.")

    with b:
        st.markdown("**With file validation**")
        if st.button("Validate uploaded file", key="run_safe_upload"):
            if uploaded is None:
                st.warning("Please upload a file first.")
            else:
                try:
                    file_bytes = uploaded.getvalue()
                    message = validate_upload(uploaded.name, file_bytes)
                    st.success(message)
                except Exception as exc:
                    st.warning(f"Rejected file: {exc}")

with tabs[8]:
    st.subheader("9) Semantic Validation")
    st.caption("Scenario: booking date must make sense relative to travel date")

    booking_date = st.text_input("Booking date (YYYY-MM-DD)", value="2026-03-01", key="book_date")
    travel_date = st.text_input("Travel date (YYYY-MM-DD)", value="2026-03-20", key="travel_date")

    a, b = st.columns(2)
    with a:
        st.markdown("**No semantic rule**")
        if st.button("Run unsafe date check", key="run_unsafe_semantic"):
            try:
                days = unsafe_trip_dates(booking_date, travel_date)
                st.success(f"Trip accepted. Lead time: {days} days")
                if days < 0:
                    st.error("System accepted impossible business data (travel before booking).")
            except Exception as exc:
                st.error(f"App crashed: {exc}")

    with b:
        st.markdown("**With semantic rule**")
        if st.button("Run safe date check", key="run_safe_semantic"):
            try:
                days = safe_trip_dates(booking_date, travel_date)
                st.success(f"Trip accepted. Lead time: {days} days")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[9]:
    st.subheader("10) Rock, Paper, Scissors Input Validation")
    st.caption("Scenario: accept only Rock, Paper, or Scissors (case-insensitive)")

    rps_input = st.text_input("Enter your choice", value="rock", key="rps_choice")

    a, b = st.columns(2)
    with a:
        st.markdown("**No validation**")
        if st.button("Run unsafe RPS input", key="run_unsafe_rps"):
            st.success(f"You entered: {rps_input}")
            st.error("Risk: invalid values like `roc`, `stone`, or blank are accepted.")

    with b:
        st.markdown("**With case-insensitive validation**")
        if st.button("Run safe RPS input", key="run_safe_rps"):
            try:
                choice = validate_rps_choice(rps_input)
                st.success(f"Validated choice: {choice}")
            except Exception as exc:
                st.warning(f"Rejected input: {exc}")

with tabs[10]:
    st.subheader("11) Theater Seating Revenue with Input Validation")
    st.markdown(
        """
**Program Description **  
A dramatic theater has three seating sections:
- Section A: 300 seats, ticket price is $20
- Section B: 500 seats, ticket price is $15
- Section C: 200 seats, ticket price is $10

The Program asks for how many tickets were sold in each section.
Then calculate and display:
- Revenue from Section A, B, and C
- Total revenue from all sections

Input validation rules:
- Each value must be a whole number
- Each value must be at least 0
- Each value cannot exceed that section's seat capacity
"""
    )

    section_prices = {"A": 20, "B": 15, "C": 10}
    section_caps = {"A": 300, "B": 500, "C": 200}

    c1, c2, c3 = st.columns(3)
    with c1:
        sold_a_raw = st.text_input(
            "Section A tickets sold (0-300)", value="120", key="theater_a"
        )
    with c2:
        sold_b_raw = st.text_input(
            "Section B tickets sold (0-500)", value="200", key="theater_b"
        )
    with c3:
        sold_c_raw = st.text_input(
            "Section C tickets sold (0-200)", value="80", key="theater_c"
        )

    if st.button("Calculate theater revenue", key="run_theater_revenue"):
        try:
            sold_a = validate_ticket_count(sold_a_raw, "A", section_caps["A"])
            sold_b = validate_ticket_count(sold_b_raw, "B", section_caps["B"])
            sold_c = validate_ticket_count(sold_c_raw, "C", section_caps["C"])

            rev_a = sold_a * section_prices["A"]
            rev_b = sold_b * section_prices["B"]
            rev_c = sold_c * section_prices["C"]
            total_rev = rev_a + rev_b + rev_c

            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.metric("Section A Revenue", f"${rev_a:,}")
            with r2:
                st.metric("Section B Revenue", f"${rev_b:,}")
            with r3:
                st.metric("Section C Revenue", f"${rev_c:,}")
            with r4:
                st.metric("Total Revenue", f"${total_rev:,}")

            st.success("Inputs are valid and revenue has been calculated.")
        except Exception as exc:
            st.warning(f"Validation error: {exc}")

st.divider()
st.markdown("## Input Validation In-Class-Assignment, Due 3/5/2026")
st.markdown("**Work in Groups of 2**")
st.markdown("**Before your print your form, make sure all the code is visible in the forms**")
st.write(
    "Open the class activity form below, complete the validation exercise, then return to this app to discuss your decisions."
)
form_path = Path(__file__).resolve().parent / "validation_exercise_final.html"
#st.caption("Reference file (app root): ./validation_exercise_final.html")
if form_path.exists():
    with st.expander("Open validation activity form", expanded=False):
        components.html(form_path.read_text(encoding="utf-8"), height=1200, scrolling=True)
else:
    st.error("validation_exercise_final.html was not found in the app root.")
