import streamlit as st

from auth import (
    get_total_users,
    get_total_logins,
    get_users,
    get_login_activity,
)


def render_admin_dashboard():

    st.title("Admin Dashboard")

    # ======================================================
    # STATISTICS
    # ======================================================

    total_users = get_total_users()
    total_logins = get_total_logins()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Registered Users",
            total_users,
        )

    with col2:
        st.metric(
            "Successful Logins",
            total_logins,
        )

    st.divider()

    # ======================================================
    # REGISTERED USERS
    # ======================================================

    st.subheader("Registered Users")

    users = get_users()

    if users:

        for user_id, email, created_at in users:

            st.write(
                f"**{email}**  \n"
                f"Registered: {created_at}"
            )

            st.divider()

    else:

        st.info("No users registered yet.")

    # ======================================================
    # LOGIN ACTIVITY
    # ======================================================

    st.subheader("Recent Login Activity")

    activity = get_login_activity()

    if activity:

        for (
            activity_id,
            user_id,
            email,
            login_time,
        ) in activity:

            st.write(
                f"**{email}**  \n"
                f"Login: {login_time}"
            )

            st.divider()

    else:

        st.info("No login activity yet.")