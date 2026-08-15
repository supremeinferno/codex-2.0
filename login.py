import streamlit as st
import textwrap
import time

from auth import (
    login_user,
    register_user,
    generate_otp,
    send_otp,
    reset_password,
    get_connection,
)


def render_login():

    # ======================================================
    # LOGIN PAGE STYLE
    # ======================================================

    st.markdown(
        """
        <style>

        /* ------------------------------------------------
           FONTS
           ------------------------------------------------ */

        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650;9..144,800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* ------------------------------------------------
           PAGE BACKDROP
           ------------------------------------------------ */

        .stApp {
            background:
                radial-gradient(
                    circle at 15% 20%,
                    rgba(212, 164, 77, 0.08),
                    transparent 34%
                ),
                radial-gradient(
                    circle at 85% 80%,
                    rgba(90, 130, 200, 0.05),
                    transparent 36%
                ),
                #0B111B;
        }

        #MainMenu,
        header,
        footer {
            visibility: hidden;
        }

        /* ------------------------------------------------
           LOGIN CARD
           ------------------------------------------------ */

        .login-card {
            max-width: 420px;
            margin: 70px auto 26px auto;

            padding: 38px 36px 30px 36px;

            background: rgba(15, 21, 33, 0.60);

            border: 1px solid rgba(212, 164, 77, 0.18);
            border-radius: 18px;

            backdrop-filter: blur(12px);

            box-shadow:
                0 10px 34px rgba(0, 0, 0, 0.32),
                0 0 0 1px rgba(212, 164, 77, 0.05) inset;

            text-align: center;

            animation: codex-login-in 0.5s ease-out;
        }

        @keyframes codex-login-in {
            from {
                opacity: 0;
                transform: translateY(8px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (prefers-reduced-motion: reduce) {
            .login-card {
                animation: none;
            }
        }

        .login-seal {
            width: 50px;
            height: 50px;

            margin: 0 auto 16px auto;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle at 35% 30%,
                    rgba(212, 164, 77, 0.30),
                    rgba(212, 164, 77, 0.06) 70%
                );

            border: 1px solid rgba(212, 164, 77, 0.55);

            box-shadow:
                0 0 18px rgba(212, 164, 77, 0.20),
                inset 0 0 10px rgba(212, 164, 77, 0.10);
        }

        .login-seal svg {
            width: 24px;
            height: 24px;
        }

        .login-logo {
            font-family: 'Fraunces', serif;

            font-size: 34px;
            font-weight: 650;
            letter-spacing: -0.5px;
            line-height: 1;
            color: #ECE8E1;
        }

        .login-x {
            color: #D4A44D;

            text-shadow:
                0 0 12px rgba(212, 164, 77, 0.28);
        }

        .login-subtitle {
            margin-top: 9px;

            color: #9C9689;

            font-size: 13px;
            letter-spacing: 0.4px;
        }

        /* ------------------------------------------------
           FORM WRAPPER
           ------------------------------------------------ */

        .login-form-wrapper {
            max-width: 420px;
            margin: 0 auto;
        }

        /* ------------------------------------------------
           TABS
           ------------------------------------------------ */

        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;

            background: rgba(17, 24, 39, 0.55);

            border: 1px solid #232C39;
            border-radius: 12px;

            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 9px;

            color: #9CA3AF;

            font-weight: 600;
            font-size: 14px;

            padding: 8px 18px;
        }

        .stTabs [aria-selected="true"] {
            background:
                linear-gradient(
                    135deg,
                    rgba(212, 164, 77, 0.20),
                    rgba(212, 164, 77, 0.08)
                ) !important;

            color: #F5EFE4 !important;

            box-shadow:
                0 0 0 1px rgba(212, 164, 77, 0.30) inset;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
        }

        /* ------------------------------------------------
           TEXT INPUTS
           ------------------------------------------------ */

        [data-testid="stTextInput"] label {
            color: #C9CDD4 !important;

            font-size: 13px !important;
            font-weight: 600 !important;
        }

        [data-testid="stTextInput"] input {
            background: rgba(17, 24, 39, 0.60) !important;

            border: 1px solid #2C3A4C !important;
            border-radius: 10px !important;

            color: #ECE8E1 !important;

            padding: 10px 14px !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: rgba(212, 164, 77, 0.60) !important;

            box-shadow:
                0 0 0 3px rgba(212, 164, 77, 0.10) !important;
        }

        /* ------------------------------------------------
           BUTTONS
           ------------------------------------------------ */

        div.stButton > button {
            width: 100%;

            min-height: 44px;

            margin-top: 6px;

            border-radius: 10px;

            border: 1px solid rgba(212, 164, 77, 0.55);

            background:
                linear-gradient(
                    135deg,
                    rgba(212, 164, 77, 0.22),
                    rgba(212, 164, 77, 0.10)
                );

            color: #F5EFE4;

            font-weight: 650;
            font-size: 14px;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                transform 0.15s ease;
        }

        div.stButton > button:hover {
            border-color: rgba(212, 164, 77, 0.85);

            box-shadow:
                0 6px 20px rgba(212, 164, 77, 0.18);

            transform: translateY(-1px);
        }

        div.stButton > button:active {
            transform: translateY(0);
        }

        /* ------------------------------------------------
           ALERTS
           ------------------------------------------------ */

        [data-testid="stAlert"] {
            border-radius: 10px;

            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        /* ------------------------------------------------
           FORGOT PASSWORD
           ------------------------------------------------ */

        .forgot-title {
            color: #9C9689;
            text-align: center;
            font-size: 13px;
            margin-top: 18px;
            margin-bottom: 8px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # CODEX HEADER
    # ======================================================

    login_header_html = """
    <div class="login-card">
        <div class="login-seal">
            <svg viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">

                <path
                    d="M12 4C10 3 6.5 2.5 3 3v15c3.5-0.5 7 0 9 1
                       2-1 5.5-1.5 9-1V3c-3.5-0.5-7 0-9 1z"
                    stroke="#D4A44D"
                    stroke-width="1.3"
                    stroke-linejoin="round"
                />

                <path
                    d="M12 4v15"
                    stroke="#D4A44D"
                    stroke-width="1.3"
                />

            </svg>
        </div>

        <div class="login-logo">
            CODE<span class="login-x">X</span>
        </div>

        <div class="login-subtitle">
            Multimodal Document Intelligence
        </div>
    </div>
    """

    login_header_html = "\n".join(
        line.strip()
        for line in login_header_html.split("\n")
        if line.strip()
    )

    st.markdown(
        login_header_html,
        unsafe_allow_html=True,
    )

    # ======================================================
    # FORM WRAPPER
    # ======================================================

    st.markdown(
        '<div class="login-form-wrapper">',
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # ======================================================
    # LOGIN
    # ======================================================

    with login_tab:

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        if st.button(
            "Login",
            use_container_width=True,
            key="login_button",
        ):

            if not email or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                success, result = login_user(
                    email,
                    password,
                )

                if success:

                    st.session_state.logged_in = True
                    st.session_state.user = result

                    st.rerun()

                else:

                    st.error(result)

        # ==================================================
        # FORGOT PASSWORD
        # ==================================================

        with st.expander("Forgot Password?"):

            reset_email = st.text_input(
                "Account Email",
                placeholder="you@example.com",
                key="reset_email",
            )

            if st.button(
                "Send OTP",
                use_container_width=True,
                key="send_otp",
            ):

                email_value = (
                    reset_email.strip().lower()
                )

                if not email_value:

                    st.error(
                        "Please enter your email."
                    )

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        SELECT id
                        FROM users
                        WHERE email = ?
                        """,
                        (email_value,),
                    )

                    user = cursor.fetchone()

                    conn.close()

                    if not user:

                        st.error(
                            "No account found with this email."
                        )

                    else:

                        otp = generate_otp()

                        success, message = send_otp(
                            email_value,
                            otp,
                        )

                        if success:

                            st.session_state.reset_target_email = (
                                email_value
                            )

                            st.session_state.reset_otp = otp

                            st.session_state.reset_otp_time = (
                                time.time()
                            )

                            st.session_state.otp_sent = True

                            st.success(
                                "OTP sent to your email."
                            )

                        else:

                            st.error(message)

            # ==============================================
            # OTP VERIFICATION
            # ==============================================

            if st.session_state.get(
                "otp_sent",
                False,
            ):

                st.markdown(
                    '<div class="forgot-title">'
                    'Enter the OTP sent to your email'
                    '</div>',
                    unsafe_allow_html=True,
                )

                otp_input = st.text_input(
                    "OTP",
                    max_chars=6,
                    placeholder="6-digit OTP",
                    key="otp_input",
                )

                new_password = st.text_input(
                    "New Password",
                    type="password",
                    placeholder="Create new password",
                    key="reset_new_password",
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Repeat new password",
                    key="reset_confirm_password",
                )

                if st.button(
                    "Reset Password",
                    use_container_width=True,
                    key="reset_password_button",
                ):

                    # OTP expiry
                    if (
                        time.time()
                        - st.session_state.reset_otp_time
                        > 300
                    ):

                        st.error(
                            "OTP expired. Please request a new one."
                        )

                    # OTP mismatch
                    elif (
                        otp_input
                        != st.session_state.reset_otp
                    ):

                        st.error(
                            "Invalid OTP."
                        )

                    # Password mismatch
                    elif (
                        new_password
                        != confirm_password
                    ):

                        st.error(
                            "Passwords do not match."
                        )

                    # Password length
                    elif len(new_password) < 6:

                        st.error(
                            "Password must contain at least 6 characters."
                        )

                    else:

                        # IMPORTANT:
                        # Use reset_target_email, NOT reset_email.
                        success, message = reset_password(
                            st.session_state.reset_target_email,
                            new_password,
                        )

                        if success:

                            # Clear OTP state
                            st.session_state.otp_sent = False
                            st.session_state.reset_otp = None
                            st.session_state.reset_target_email = None
                            st.session_state.reset_otp_time = None

                            st.success(
                                "Password reset successfully."
                            )

                            st.info(
                                "You can now login with your new password."
                            )

                        else:

                            st.error(message)

    # ======================================================
    # CREATE ACCOUNT
    # ======================================================

    with register_tab:

        new_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="register_email",
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Repeat your password",
            key="register_confirm_password",
        )

        if st.button(
            "Create Account",
            use_container_width=True,
            key="register_button",
        ):

            if not new_email or not new_password:

                st.error(
                    "Please enter your email and password."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                success, message = register_user(
                    new_email,
                    new_password,
                )

                if success:

                    st.success(message)

                    st.info(
                        "Your account is ready. "
                        "Open the Login tab to continue."
                    )

                else:

                    st.error(message)

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )