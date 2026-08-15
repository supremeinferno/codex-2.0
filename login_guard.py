import streamlit as st

from login import render_login


def require_login():
    if not st.session_state.get("logged_in", False):

        render_login()

        st.stop()