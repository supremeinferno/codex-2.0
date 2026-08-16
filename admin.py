import streamlit as st

from auth import (
    get_total_users,
    get_total_logins,
    get_users,
    get_login_activity,
    delete_user,
    clear_login_activity,
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

        with st.container(
            height=300,
            border=True,
        ):

            for user_id, email, created_at in users:

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(
                        f"**{email}**  \n"
                        f"Registered: {created_at}"
                    )

                with col2:

                    if st.button(
                        "Remove",
                        key=f"remove_user_{user_id}",
                        type="secondary",
                    ):

                        delete_user(user_id)

                        st.rerun()

                st.divider()

    else:

        st.info(
            "No users registered yet."
        )

    # ======================================================
    # LOGIN ACTIVITY
    # ======================================================

    st.subheader("Recent Login Activity")

    activity = get_login_activity()

    if activity:

        if st.button(
            "Clear Login Activity",
            key="clear_login_activity",
            type="secondary",
        ):

            st.session_state.confirm_clear_logins = True

        if st.session_state.get(
            "confirm_clear_logins",
            False,
        ):

            st.warning(
                "This will permanently delete "
                "all login activity."
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:

                if st.button(
                    "Yes, Clear All",
                    key="confirm_clear_all_logins",
                    type="primary",
                    use_container_width=True,
                ):

                    clear_login_activity()

                    st.session_state.confirm_clear_logins = False

                    st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key="cancel_clear_logins",
                    use_container_width=True,
                ):

                    st.session_state.confirm_clear_logins = False

                    st.rerun()

        # Scrollable login activity box
        with st.container(
            height=300,
            border=True,
        ):

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

        st.info(
            "No login activity yet."
        )