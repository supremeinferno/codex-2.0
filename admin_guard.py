import streamlit as st

ADMIN_EMAIL = "317madhavgarg@gmail.com"


def require_admin():

    user = st.session_state.get("user")

    if not st.session_state.get("logged_in", False):
        st.error("Please login first.")
        st.stop()

    if not user or user.get("email") != ADMIN_EMAIL:
        st.error("Access denied. Admin privileges required.")
        st.stop()