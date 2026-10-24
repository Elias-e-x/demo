"""
Cedar Roasters demo: an HTML dashboard behind a login screen.

Visitors who are not logged in only see a welcome screen.
After logging in (or signing up) through Auth0, they see the dashboard.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ---- Settings you may want to change ----
APP_NAME = "Cedar Roasters Dashboard"
DASHBOARD_FILE = Path(__file__).parent / "dashboard" / "dashboard.html"
DASHBOARD_HEIGHT = 1150  # pixels; increase if your dashboard gets cut off

st.set_page_config(page_title=APP_NAME, page_icon="☕", layout="wide")

# Reduce Streamlit's default padding so the dashboard fills the page
st.markdown(
    """
    <style>
      .block-container, [data-testid="stMainBlockContainer"] {
        padding-top: 2.5rem;
        padding-bottom: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def auth_is_configured() -> bool:
    """True if the [auth] section exists in secrets."""
    try:
        return "auth" in st.secrets
    except Exception:
        return False


# ---- 1. Make sure login is set up ----
if not auth_is_configured():
    st.error(
        "Login isn't configured yet. Add the [auth] section to your secrets: "
        "locally in .streamlit/secrets.toml, or on Streamlit Cloud under "
        "App settings → Secrets. See README.md, step 3."
    )
    st.stop()

# ---- 2. Welcome screen for visitors who are not logged in ----
if not st.user.is_logged_in:
    _, middle, _ = st.columns([1, 2, 1])
    with middle:
        st.title(APP_NAME)
        st.write(
            "Log in to view the dashboard. "
            "If you don't have an account yet, you can create one on the next screen."
        )
        st.button("Log in / Sign up", type="primary", on_click=st.login)
    st.stop()  # nothing below this line runs for logged-out visitors

# ---- 3. Logged-in users ----
with st.sidebar:
    st.write("Signed in as")
    st.markdown(f"**{st.user.get('name') or st.user.get('email', 'User')}**")
    if st.user.get("email"):
        st.caption(st.user.get("email"))
    st.button("Log out", on_click=st.logout)


@st.cache_data
def load_dashboard(path: str, modified: float) -> str:
    # 'modified' makes the cache refresh whenever the file changes
    return Path(path).read_text(encoding="utf-8")


if not DASHBOARD_FILE.exists():
    st.error(f"Dashboard file not found: {DASHBOARD_FILE.relative_to(Path(__file__).parent)}")
    st.stop()

html = load_dashboard(str(DASHBOARD_FILE), DASHBOARD_FILE.stat().st_mtime)
components.html(html, height=DASHBOARD_HEIGHT, scrolling=True)
