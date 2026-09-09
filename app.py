import streamlit as st


st.set_page_config(page_title="ITP100 Course App", page_icon="📘", layout="wide")

pages = [
    st.Page("module_pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("module_pages/api_tester.py", title="API Tester", icon="🧪"),
    st.Page("module_pages/module7_input_validation.py", title="Module 7 - Input Validation", icon="✅"),
    st.Page("module_pages/module8_arrays.py", title="Module 8 - Arrays", icon="🧮"),
    st.Page("module_pages/module8_arrays_react.py", title="Module 8 - Arrays (React Activities)", icon="⚛️"),
    st.Page("module_pages/chatbot_demo.py", title="Chatbot Demo", icon="💬"),
]

navigator = st.navigation(pages)
navigator.run()
