import streamlit as st

from admin_guard import require_admin
from admin import render_admin_dashboard


def render_admin_page():

    require_admin()

    render_admin_dashboard()