import streamlit as st


def is_logged_in():
    return st.session_state.get("logged_in", False)


def get_current_user():
    return st.session_state.get("user")


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None