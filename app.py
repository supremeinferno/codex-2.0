import streamlit as st
from pages.individual import render_individual
# from pages.dashboard import render_dashboard

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
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 22px 0;
    border-bottom: 1px solid #232C38;
    margin-bottom: 35px;
}

.logo {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #ECE8E1;
    line-height: 1;
}

.logo span {
    color: #D4A44D;
}

.subtitle {
    color: #9CA3AF;
    font-size: 13px;
    margin-top: 8px;
    letter-spacing: 0.3px;
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
   INFO BOX
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

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# NAVBAR
# ==========================================================

# IMPORTANT:
# HTML is intentionally written without indentation so
# Streamlit's Markdown parser cannot interpret it as code.

st.markdown(
    '<div class="navbar"><div><div class="logo">CODE<span>X</span></div><div class="subtitle">Multimodal Document Intelligence</div></div></div>',
    unsafe_allow_html=True,
)


# ==========================================================
# WORKSPACE NAVIGATION
# ==========================================================

st.markdown(
    '<div class="workspace-title">Workspace</div>',
    unsafe_allow_html=True,
)

nav1, nav2, nav3 = st.columns(3, gap="medium")


with nav1:

    if st.button(
        "Individual Analysis",
        key="nav_individual",
    ):
        st.session_state.current_page = "Individual Analysis"


with nav2:

    if st.button(
        "Research Mode",
        key="nav_research",
    ):
        st.session_state.current_page = "Research Mode"


with nav3:

    if st.button(
        "Dashboard",
        key="nav_dashboard",
    ):
        st.session_state.current_page = "Dashboard"


st.divider()



# ==========================================================
# PAGE ROUTER
# ==========================================================

current_page = st.session_state.current_page


# ==========================================================
# INDIVIDUAL ANALYSIS
# ==========================================================

if current_page == "Individual Analysis":

    render_individual()


# ==========================================================
# RESEARCH MODE
# ==========================================================

elif current_page == "Research Mode":

    st.markdown(
        '<div class="page-title">Research Mode</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Analyze multiple documents as a unified research corpus '
        'and perform cross-document reasoning.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Research Mode module will be connected next."
    )


# ==========================================================
# DASHBOARD
# ==========================================================

elif current_page == "Dashboard":

    st.markdown(
        '<div class="page-title">Dashboard</div>',
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
        "Dashboard module will be connected next."
    )