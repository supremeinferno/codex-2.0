import streamlit as st

from pages.individual import render_individual


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Codex",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Individual Analysis"


# ==========================================================
# GLOBAL CSS
# ==========================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background: #0B111B;
    color: #ECE8E1;
}

#MainMenu,
header,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ==========================================================
   NAVBAR
   ========================================================== */

.navbar {
    width: 100%;
    padding: 10px 0 24px 0;
    margin-bottom: 32px;
    border-bottom: 1px solid #232C38;
}

.logo {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1;
    color: #ECE8E1;
}

.logo span {
    color: #D4A44D;
}

.subtitle {
    margin-top: 9px;
    color: #9CA3AF;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 0.3px;
    line-height: 1.4;
}


/* ==========================================================
   WORKSPACE
   ========================================================== */

.workspace-title {
    font-size: 24px;
    font-weight: 700;

    color: #ECE8E1;

    margin-bottom: 15px;
}


/* ==========================================================
   PAGE
   ========================================================== */

.page-title {
    font-size: 46px;
    font-weight: 750;

    letter-spacing: -1.5px;

    color: #ECE8E1;

    margin-top: 38px;
    margin-bottom: 8px;
}

.page-description {
    color: #9CA3AF;

    font-size: 16px;

    line-height: 1.7;

    max-width: 850px;

    margin-bottom: 28px;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {

    width: 100%;

    min-height: 46px;

    border-radius: 11px;

    border: 1px solid #2A3441;

    background: #111827;

    color: #ECE8E1;

    font-size: 14px;

    font-weight: 600;

    transition: all 0.2s ease;
}

.stButton > button:hover {

    border-color: #D4A44D;

    background: #151E2B;

    color: #D4A44D;
}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {

    background: #111827;

    border: 1px solid #2A3441;

    border-radius: 11px;

    padding: 8px;
}


/* ==========================================================
   INPUT
   ========================================================== */

[data-testid="stChatInput"] {

    border-color: #2A3441;
}


/* ==========================================================
   INFO / ALERT
   ========================================================== */

[data-testid="stAlert"] {

    border-radius: 12px;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border-color: #232C38 !important;
}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {

    width: 7px;
}

::-webkit-scrollbar-track {

    background: #0B111B;
}

::-webkit-scrollbar-thumb {

    background: #2A3441;

    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {

    background: #3A4656;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# NAVBAR
# ==========================================================

st.markdown(
    """
    <div style="
        padding: 10px 0 22px 0;
        margin-bottom: 30px;
        border-bottom: 1px solid #232C38;
    ">

        <div style="
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -1.5px;
            line-height: 1;
            color: #ECE8E1;
        ">
            CODE<span style="color: #D4A44D;">X</span>
        </div>

        <div style="
            color: #9CA3AF;
            font-size: 13px;
            font-weight: 400;
            margin-top: 9px;
            letter-spacing: 0.3px;
            line-height: 1.4;
        ">
            Multimodal Document Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# WORKSPACE NAVIGATION
# ==========================================================

st.markdown(
    '<div class="workspace-title">Workspace</div>',
    unsafe_allow_html=True,
)


nav1, nav2, nav3 = st.columns(
    3,
    gap="medium"
)


# ==========================================================
# INDIVIDUAL ANALYSIS BUTTON
# ==========================================================

with nav1:

    if st.button(
        "Individual Analysis",
        key="nav_individual",
        use_container_width=True,
    ):

        st.session_state.current_page = (
            "Individual Analysis"
        )

        st.rerun()


# ==========================================================
# RESEARCH MODE BUTTON
# ==========================================================

with nav2:

    if st.button(
        "Research Mode",
        key="nav_research",
        use_container_width=True,
    ):

        st.session_state.current_page = (
            "Research Mode"
        )

        st.rerun()


# ==========================================================
# DASHBOARD BUTTON
# ==========================================================

with nav3:

    if st.button(
        "Dashboard",
        key="nav_dashboard",
        use_container_width=True,
    ):

        st.session_state.current_page = (
            "Dashboard"
        )

        st.rerun()


# ==========================================================
# DIVIDER
# ==========================================================

st.divider()


# ==========================================================
# PAGE ROUTER
# ==========================================================

current_page = st.session_state.current_page


# ==========================================================
# INDIVIDUAL ANALYSIS
# ==========================================================

if current_page == "Individual Analysis":

    st.markdown(
        '<div class="page-title">'
        'Individual Analysis'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Analyze a single document or image using '
        'multimodal retrieval and generation.'
        '</div>',
        unsafe_allow_html=True,
    )

    render_individual()


# ==========================================================
# RESEARCH MODE
# ==========================================================

elif current_page == "Research Mode":

    st.markdown(
        '<div class="page-title">'
        'Research Mode'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Analyze multiple documents as a unified '
        'research corpus and perform cross-document reasoning.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Research Mode is under development."
    )


# ==========================================================
# DASHBOARD
# ==========================================================

elif current_page == "Dashboard":

    st.markdown(
        '<div class="page-title">'
        'Dashboard'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Monitor Codex usage, processing performance, '
        'document activity, and analytics.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Dashboard is under development."
    )