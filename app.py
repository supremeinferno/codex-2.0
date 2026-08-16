import streamlit as st
from login_guard import require_login
from profile import render_profile
from pages.individual import render_individual
from admin_page import render_admin_page

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Codex",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# LOGIN CHECK
require_login()


# ==========================================================
# GLOBAL UI
# ==========================================================

st.markdown(
    """
    <style>

    /* ======================================================
       FONTS

       Fraunces  -> display / wordmark / headings
       Inter     -> body & UI text
       JetBrains Mono -> code snippets
       ====================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650;9..144,800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    code, pre, kbd {
        font-family: 'JetBrains Mono', monospace !important;
    }


    /* ======================================================
       APP
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 10%,
                rgba(212, 164, 77, 0.07),
                transparent 32%
            ),
            radial-gradient(
                circle at 92% 18%,
                rgba(90, 130, 200, 0.05),
                transparent 34%
            ),
            radial-gradient(
                ellipse at 50% 100%,
                rgba(212, 164, 77, 0.03),
                transparent 60%
            ),
            #0B111B;

        color: #ECE8E1;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;

        animation: codex-fade-in 0.5s ease-out;
    }

    @keyframes codex-fade-in {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .block-container {
            animation: none;
        }
    }

    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }


    /* ======================================================
       NAVBAR
       ====================================================== */

    .codex-navbar {
        display: flex;
        align-items: center;
        gap: 16px;

        padding: 6px 0 26px 0;
        margin-bottom: 30px;

        border-bottom: 1px solid rgba(212, 164, 77, 0.30);

        box-shadow:
            0 1px 10px rgba(212, 164, 77, 0.08);
    }

    .codex-seal {
        flex-shrink: 0;

        width: 46px;
        height: 46px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 35% 30%,
                rgba(212, 164, 77, 0.28),
                rgba(212, 164, 77, 0.06) 70%
            );

        border: 1px solid rgba(212, 164, 77, 0.55);

        box-shadow:
            0 0 16px rgba(212, 164, 77, 0.18),
            inset 0 0 10px rgba(212, 164, 77, 0.10);
    }

    .codex-seal svg {
        width: 22px;
        height: 22px;
    }

    .codex-logo {
        font-family: 'Fraunces', serif;
        font-optical-sizing: auto;

        font-size: 32px;
        font-weight: 650;
        letter-spacing: -0.5px;
        line-height: 1;
        color: #ECE8E1;
    }

    .codex-x {
        color: #D4A44D;
        text-shadow:
            0 0 12px rgba(212, 164, 77, 0.28);
    }

    .codex-subtitle {
        color: #9C9689;
        font-size: 13px;
        font-weight: 400;
        margin-top: 6px;
        letter-spacing: 0.4px;
    }


    /* ======================================================
       WORKSPACE
       ====================================================== */

    .workspace-title {
        font-family: 'Fraunces', serif;

        font-size: 20px;
        font-weight: 600;
        color: #ECE8E1;
        margin-bottom: 14px;

        letter-spacing: 0.2px;
    }


    /* ======================================================
       NAVIGATION BUTTONS
       ====================================================== */

    div.stButton > button {

        width: 100%;
        min-height: 46px;

        border-radius: 12px;

        border: 1px solid #232C39;

        background: rgba(17, 24, 39, 0.62);

        color: #C9CDD4;

        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.1px;

        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            box-shadow 0.2s ease,
            transform 0.15s ease,
            color 0.2s ease;
    }

    div.stButton > button:hover {

        border-color: rgba(212, 164, 77, 0.6);

        background: rgba(25, 32, 45, 0.92);

        color: #F2EEE8;

        box-shadow:
            0 4px 16px rgba(212, 164, 77, 0.10);

        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Active page — Streamlit's primary button variant */

    div.stButton > button[kind="primary"] {

        border: 1px solid rgba(212, 164, 77, 0.85);

        background:
            linear-gradient(
                135deg,
                rgba(212, 164, 77, 0.20),
                rgba(212, 164, 77, 0.08)
            );

        color: #F5EFE4;

        box-shadow:
            0 0 0 1px rgba(212, 164, 77, 0.12) inset,
            0 4px 18px rgba(212, 164, 77, 0.16);
    }

    div.stButton > button[kind="primary"]:hover {

        border-color: rgba(212, 164, 77, 0.95);

        box-shadow:
            0 0 0 1px rgba(212, 164, 77, 0.18) inset,
            0 6px 22px rgba(212, 164, 77, 0.22);

        transform: translateY(-1px);
    }


    /* ======================================================
       GLASS PANELS (bordered containers, e.g. Dialogue box)
       ====================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background: rgba(15, 21, 33, 0.55) !important;

        border: 1px solid rgba(212, 164, 77, 0.16) !important;
        border-radius: 16px !important;

        backdrop-filter: blur(10px);

        box-shadow:
            0 8px 28px rgba(0, 0, 0, 0.28);
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {

        border: none !important;

        height: 1px !important;

        margin: 26px 0 !important;

        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(212, 164, 77, 0.12) 15%,
            rgba(212, 164, 77, 0.58) 50%,
            rgba(212, 164, 77, 0.12) 85%,
            transparent 100%
        ) !important;

        box-shadow:
            0 0 6px rgba(212, 164, 77, 0.20),
            0 0 14px rgba(212, 164, 77, 0.06);
    }


    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {

        background: rgba(17, 24, 39, 0.50);

        border: 1px dashed #2C3A4C;

        border-radius: 14px;

        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            box-shadow 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover {

        border-color: rgba(212, 164, 77, 0.55);

        background: rgba(20, 27, 41, 0.65);

        box-shadow:
            0 0 18px rgba(212, 164, 77, 0.08);
    }


    /* ======================================================
       CHAT INPUT
       ====================================================== */

    [data-testid="stChatInput"] {

        border-color: #2C3A4C !important;

        border-radius: 12px !important;

        background: rgba(17, 24, 39, 0.55) !important;
    }

    [data-testid="stChatInput"]:focus-within {

        border-color: rgba(212, 164, 77, 0.6) !important;

        box-shadow:
            0 0 0 3px rgba(212, 164, 77, 0.10) !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {

        border-radius: 12px;

        border: 1px solid rgba(255, 255, 255, 0.06);
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3 {
        font-family: 'Fraunces', serif;

        color: #ECE8E1 !important;
    }


    /* ======================================================
       SCROLLBAR
       ====================================================== */

    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {

        background: rgba(212, 164, 77, 0.30);

        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {

        background: rgba(212, 164, 77, 0.55);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Individual Analysis"


# ==========================================================
# NAVBAR
# ==========================================================

st.markdown(
    """
    <div class="codex-navbar">
        <div class="codex-seal">
            <svg viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
                <path d="M12 4C10 3 6.5 2.5 3 3v15c3.5-0.5 7 0 9 1
                         2-1 5.5-1.5 9-1V3c-3.5-0.5-7 0-9 1z"
                      stroke="#D4A44D" stroke-width="1.3"
                      stroke-linejoin="round"/>
                <path d="M12 4v15" stroke="#D4A44D"
                      stroke-width="1.3"/>
            </svg>
        </div>
        <div>
            <div class="codex-logo">
                CODE<span class="codex-x">X</span>
            </div>
            <div class="codex-subtitle">
                Multimodal Document Intelligence
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# WORKSPACE
# ==========================================================


# PROFILE
render_profile()


st.markdown(
    '<div class="workspace-title">Workspace</div>',
    unsafe_allow_html=True,
)


# ==========================================================
# NAVIGATION
# ==========================================================

nav1, nav2= st.columns(
    2,
    gap="medium",
)


def _nav_button_type(page_name: str) -> str:

    if st.session_state.current_page == page_name:
        return "primary"

    return "secondary"


with nav1:

    if st.button(
        "🗂️  Individual Analysis",
        key="nav_individual",
        use_container_width=True,
        type=_nav_button_type("Individual Analysis"),
    ):

        st.session_state.current_page = (
            "Individual Analysis"
        )

        st.rerun()


with nav2:

    if st.button(
        "🔎  Research Mode",
        key="nav_research",
        use_container_width=True,
        type=_nav_button_type("Research Mode"),
    ):

        st.session_state.current_page = (
            "Research Mode"
        )

        st.rerun()




# ==========================================================
# ADMIN NAVIGATION
# ==========================================================

# ==========================================================
# ADMIN NAVIGATION
# ==========================================================

ADMIN_EMAIL = "pgarg_be24@thapar.edu"

user = st.session_state.get("user")

if (
    user
    and user.get("email", "").strip().lower()
    == ADMIN_EMAIL.strip().lower()
):

    if st.button(
        "Admin Dashboard",
        key="nav_admin",
        use_container_width=True,
    ):

        st.session_state.current_page = "Admin Dashboard"
        st.rerun()


# ==========================================================
# PAGE ROUTER
# ==========================================================

if st.session_state.current_page == "Individual Analysis":

    render_individual()


elif st.session_state.current_page == "Research Mode":

    st.title("Research Mode")

    st.info(
        "Research Mode is under development."
    )


elif st.session_state.current_page == "Admin Dashboard":

    render_admin_page()