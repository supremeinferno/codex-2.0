import streamlit as st

from session import get_current_user, logout


def render_profile():

    user = get_current_user()

    if not user:
        return

    col1, col2 = st.columns([4, 1])

    with col1:
        st.caption(
            f"Signed in as {user['email']}"
        )

    with col2:

        if st.button(
            "Logout",
            key="logout_button",
            use_container_width=True,
        ):
            logout()
            st.rerun()