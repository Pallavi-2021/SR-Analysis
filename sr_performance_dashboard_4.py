# -*- coding: utf-8 -*-
"""
SR Performance Analytics Dashboard
====================================
Run:  streamlit run app.py
Deps: pip install streamlit plotly pandas numpy chardet openpyxl xlrd
"""

import io
import warnings
import chardet
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SR Performance Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# GLOBAL CSS  --  all fonts bold black, no emojis, professional look
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&display=swap');

/* ===== GLOBAL BASE ===== */
html, body, [class*="css"], p, span, div, label, li,
td, th, h1, h2, h3, h4, h5, button, input, select, textarea {
    font-family: 'Inter', sans-serif !important;
    color: #000000 !important;
    font-weight: 700 !important;
}
.stApp { background: #eef2f7; }

/* Main content area white card feel */
.main .block-container {
    background: transparent;
    padding-top: 2rem;
}

/* ===== MAIN AREA TEXT ===== */
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #000000 !important; font-weight: 700 !important;
}
.stDataFrame td, .stDataFrame th {
    color: #000000 !important; font-weight: 700 !important;
}
.stAlert p { color: #000000 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #000000 !important; font-weight: 800 !important; }
[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 900 !important; }
[data-testid="stDataFrame"] * { font-weight: 700 !important; color: #000 !important; }
.stTabs [role="tab"] { font-weight: 800 !important; color: #000 !important; }

/* Main area selectbox / multiselect labels */
.stSelectbox label, .stMultiSelect label,
.stFileUploader label, .stTextInput label {
    color: #000000 !important; font-weight: 800 !important; font-size: 13px !important;
}

/* ===== SIDEBAR SHELL ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* All sidebar text white by default */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Sidebar section labels (UPLOAD DATA, FILTERS) */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stFileUploader label {
    color: #cbd5e1 !important;
    font-weight: 800 !important;
    font-size: 12px !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 4px !important;
}

/* ===== SIDEBAR DROPDOWNS / SELECTBOX ===== */
/* The visible selected-value box */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:hover {
    background-color: #ffffff !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 8px !important;
}
/* Text inside the closed selectbox */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}
/* Dropdown arrow icon */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] svg {
    fill: #1d4ed8 !important;
}

/* ===== SIDEBAR MULTISELECT ===== */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] span,
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] div {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}
/* Selected tags inside multiselect */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #1d4ed8 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ===== GLOBAL DROPDOWN POPUP (renders outside sidebar DOM) ===== */
[data-baseweb="popover"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.14) !important;
}
[data-baseweb="popover"] ul li,
[data-baseweb="popover"] [role="option"] {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    background: #ffffff !important;
}
[data-baseweb="popover"] ul li:hover,
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
}

/* ===== FILE UPLOADER IN SIDEBAR ===== */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px dashed rgba(148,163,184,0.5) !important;
    border-radius: 8px !important;
    padding: 6px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
[data-testid="stSidebar"] [data-testid="stFileUploader"] p {
    color: #94a3b8 !important;
    font-size: 11px !important;
}
/* The browse button inside the uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background: #1e40af !important;
}

/* ===== SUCCESS / ERROR ALERTS IN SIDEBAR ===== */
[data-testid="stSidebar"] .stSuccess {
    background: rgba(21,128,61,0.18) !important;
    border-left: 3px solid #15803d !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stSuccess p {
    color: #bbf7d0 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .stError {
    background: rgba(185,28,28,0.18) !important;
    border-left: 3px solid #b91c1c !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stError p {
    color: #fecaca !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}

/* ===== KPI CARDS ===== */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 22px 16px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.06);
    border-top: 5px solid;
    min-height: 112px;
    transition: box-shadow 0.2s ease;
}
.kpi-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.13);
}
.kpi-card.blue   { border-color: #1d4ed8; }
.kpi-card.green  { border-color: #15803d; }
.kpi-card.amber  { border-color: #b45309; }
.kpi-card.red    { border-color: #b91c1c; }
.kpi-card.purple { border-color: #6d28d9; }
.kpi-label {
    font-size: 10px !important; font-weight: 800 !important;
    color: #64748b !important; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 8px;
}
.kpi-value {
    font-size: 30px !important; font-weight: 900 !important;
    color: #000000 !important; line-height: 1.1;
}
.kpi-delta { font-size: 12px !important; font-weight: 700 !important; margin-top: 6px; }
.kpi-delta.up   { color: #15803d !important; }
.kpi-delta.down { color: #b91c1c !important; }

/* ===== SECTION HEADERS ===== */
.sec-hdr {
    background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%);
    color: #ffffff !important;
    padding: 11px 20px;
    border-radius: 8px;
    font-size: 13px !important;
    font-weight: 800 !important;
    margin: 32px 0 12px 0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 2px 8px rgba(29,78,216,0.25);
}

/* ===== INSIGHT BOXES ===== */
.ins-box {
    background: #f0f7ff;
    border-left: 5px solid #1d4ed8;
    border-radius: 0 8px 8px 0;
    padding: 13px 18px;
    margin: 6px 0 20px 0;
    font-size: 13px !important;
    color: #1e293b !important;
    font-weight: 700 !important;
    line-height: 1.7;
}
.ins-box strong { color: #1d4ed8 !important; font-weight: 900 !important; }

/* ===== UPLOAD LANDING PANEL ===== */
.up-panel {
    background: #ffffff;
    border-radius: 16px;
    padding: 40px 36px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
    border: 2px dashed #93c5fd;
    text-align: center;
}

/* ===== PAGE TITLES ===== */
.pg-title {
    font-size: 24px !important;
    font-weight: 900 !important;
    color: #000000 !important;
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}
.pg-sub {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #475569 !important;
    margin-bottom: 24px;
    line-height: 1.5;
}

/* ===== DIVIDER ===== */
hr { border-color: rgba(255,255,255,0.1) !important; }

/* ===== LOG BADGES ===== */
.log-ok {
    display: inline-block; background: #dcfce7; color: #166534 !important;
    font-weight: 800 !important; font-size: 12px !important;
    border-radius: 20px; padding: 4px 14px; margin: 4px 3px;
    border: 1px solid #bbf7d0;
}
.log-warn {
    display: inline-block; background: #fef9c3; color: #854d0e !important;
    font-weight: 800 !important; font-size: 12px !important;
    border-radius: 20px; padding: 4px 14px; margin: 4px 3px;
    border: 1px solid #fde68a;
}

/* ===== COLUMN INFO TABLE ===== */
.col-table {
    background: #ffffff; border-radius: 12px; padding: 24px 26px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* ===== BOTTOM NAV STREAMLIT BUTTONS ===== */
/* Previous button -- grey, left aligned */
[data-testid="stHorizontalBlock"] > div:first-child .stButton button {
    background: #f1f5f9 !important;
    color: #374151 !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    padding: 10px 20px !important;
}
[data-testid="stHorizontalBlock"] > div:first-child .stButton button:hover {
    background: #e2e8f0 !important;
    border-color: #cbd5e1 !important;
}
/* Next button -- blue, right aligned */
[data-testid="stHorizontalBlock"] > div:last-child .stButton button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: 2px solid #1d4ed8 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    padding: 10px 20px !important;
}
[data-testid="stHorizontalBlock"] > div:last-child .stButton button:hover {
    background: #1e40af !important;
    border-color: #1e40af !important;
}

/* ===== SIDEBAR NAV BUTTONS ===== */
[data-testid="stSidebar"] .stButton button {
    border-radius: 7px !important;
    padding: 8px 12px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-align: left !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    background: rgba(255,255,255,0.07) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(59,130,246,0.25) !important;
    color: #ffffff !important;
    border-color: rgba(59,130,246,0.5) !important;
}

/* ===== DATAFRAME STYLE ===== */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# PLOTLY STYLE HELPERS
# ---------------------------------------------------------------------------
FONT = dict(family="Inter", size=13, color="#000000")
AXIS = dict(
    tickfont=dict(family="Inter", size=12, color="#000000"),
    title_font=dict(family="Inter", size=13, color="#000000"),
    showgrid=True,
    gridcolor="#e2e8f0",
)
LAY = dict(
    font=FONT,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    legend=dict(font=dict(family="Inter", size=12, color="#000000")),
    margin=dict(t=30, b=50, l=55, r=25),
)


def sfig(fig, h=380, leg=True):
    fig.update_layout(height=h, **LAY)
    fig.update_xaxes(**AXIS)
    fig.update_yaxes(**AXIS)
    if leg:
        fig.update_layout(
            legend=dict(orientation="h", y=-0.28,
                        font=dict(family="Inter", size=12, color="#000000"))
        )
    return fig


# ---------------------------------------------------------------------------
# UI HELPERS
# ---------------------------------------------------------------------------
def kpi(label, value, delta=None, dir_="up", color="blue"):
    d = f'<div class="kpi-delta {dir_}">{delta}</div>' if delta else ""
    st.markdown(
        f'<div class="kpi-card {color}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>{d}</div>',
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)


def insight(text):
    st.markdown(
        f'<div class="ins-box"><strong>How to read this:</strong> {text}</div>',
        unsafe_allow_html=True,
    )


def nav_buttons():
    """Render a clean bottom navigation bar using only native Streamlit components."""
    cur   = st.session_state["current_page"]
    total = len(PAGES)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<hr style="border:none;border-top:2px solid #e2e8f0;margin:8px 0 16px 0;">',
        unsafe_allow_html=True,
    )

    # Build dot indicators as a single safe HTML string (no nested f-strings)
    dot_parts = []
    for i in range(total):
        if i == cur:
            dot_parts.append(
                '<span style="display:inline-block;width:22px;height:8px;'
                'border-radius:4px;background:#1d4ed8;margin:0 3px;"></span>'
            )
        else:
            dot_parts.append(
                '<span style="display:inline-block;width:8px;height:8px;'
                'border-radius:50%;background:#cbd5e1;margin:0 3px;"></span>'
            )
    dots_html = "".join(dot_parts)

    page_label = (
        '<div style="text-align:center;margin-bottom:12px;">'
        + dots_html
        + '<div style="font-size:12px;font-weight:700;color:#64748b;margin-top:8px;">'
        + f"Page {cur + 1} of {total}  --  {PAGES[cur]}"
        + "</div></div>"
    )
    st.markdown(page_label, unsafe_allow_html=True)

    col_prev, col_mid, col_next = st.columns([3, 4, 3])

    with col_prev:
        if cur > 0:
            if st.button(
                f"Previous: {PAGES[cur - 1]}",
                key="nav_prev",
                use_container_width=True,
            ):
                st.session_state["current_page"] = cur - 1
                st.rerun()

    with col_mid:
        st.empty()

    with col_next:
        if cur < total - 1:
            if st.button(
                f"Next: {PAGES[cur + 1]}",
                key="nav_next",
                use_container_width=True,
            ):
                st.session_state["current_page"] = cur + 1
                st.rerun()


# ---------------------------------------------------------------------------
# ROBUST FILE READER  --  handles any CSV encoding automatically
# ---------------------------------------------------------------------------
def read_file(uploaded_file):
    """
    Reads CSV or Excel files uploaded via st.file_uploader.

    CSV encoding strategy:
      1. Read raw bytes into memory.
      2. Use chardet to detect the encoding.
      3. Try the detected encoding first, then fall back through a list of
         common encodings used in Excel exports across all locales.
      4. on_bad_lines='skip' tolerates any remaining corrupt rows.

    Excel (.xlsx / .xls):
      Binary formats have no encoding issues -- read directly.
    """
    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()

    if name.endswith(".csv"):
        detected   = chardet.detect(raw_bytes)
        enc_guess  = (detected.get("encoding") or "utf-8").strip()
        confidence = detected.get("confidence", 0)

        # Priority order: detected encoding first (if confident), then fallbacks
        priority = []
        if confidence and confidence > 0.4:
            priority.append(enc_guess)

        fallbacks = [
            "utf-8-sig",   # UTF-8 with BOM (very common from Excel)
            "utf-8",
            "latin-1",     # covers 0xfd and most Western European chars
            "cp1252",      # Windows Western European
            "iso-8859-1",
            "cp1250",      # Windows Central European
            "cp1256",      # Windows Arabic
            "cp1251",      # Windows Cyrillic
            "utf-16",
            "utf-16-le",
            "utf-16-be",
        ]
        for enc in fallbacks:
            if enc.lower() not in [x.lower() for x in priority]:
                priority.append(enc)

        last_err = None
        for enc in priority:
            try:
                df = pd.read_csv(
                    io.BytesIO(raw_bytes),
                    encoding=enc,
                    on_bad_lines="skip",
                    low_memory=False,
                )
                return df
            except (UnicodeDecodeError, LookupError) as exc:
                last_err = exc
                continue

        raise ValueError(
            f"Could not read the CSV file after trying all encodings. "
            f"Last error: {last_err}. "
            "Please re-save the file as 'CSV UTF-8 (Comma delimited)' from Excel."
        )

    elif name.endswith(".xlsx"):
        return pd.read_excel(io.BytesIO(raw_bytes), engine="openpyxl")

    elif name.endswith(".xls"):
        return pd.read_excel(io.BytesIO(raw_bytes), engine="xlrd")

    else:
        raise ValueError(
            f"Unsupported file type: '{uploaded_file.name}'. "
            "Please upload a CSV, XLSX, or XLS file."
        )


# ---------------------------------------------------------------------------
# COLUMN NAME NORMALISER
# ---------------------------------------------------------------------------
def find_col(df, candidates):
    """Case- and whitespace-insensitive column lookup."""
    lookup = {c.lower().replace(" ", "").replace("_", ""): c for c in df.columns}
    for cand in candidates:
        k = cand.lower().replace(" ", "").replace("_", "")
        if k in lookup:
            return lookup[k]
    return None


# ---------------------------------------------------------------------------
# PREPROCESS -- PLANNED VISITS
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Preprocessing planned visits...")
def preprocess_planned(raw):
    df = raw.copy()
    df.columns = df.columns.str.strip()
    log = []

    col_map = {
        "DistributorCode": ["DistributorCode", "Distributor Code", "dist_code", "DistCode"],
        "DistributorName": ["DistributorName", "Distributor Name", "dist_name", "Distributor"],
        "SRCode":          ["SRCode", "SR Code", "sr_code", "SalesRepCode", "SR"],
        "SRName":          ["SRName", "SR Name", "sr_name", "SalesRepName", "RepName"],
        "Date":            ["Date", "date", "Visit Date", "VisitDate", "planned_date"],
        "StoreID":         ["StoreID", "Store ID", "store_id", "Store", "ShopID"],
        "PlannedCalls":    ["PlannedCalls", "Planned Calls", "planned_calls", "Calls"],
    }
    ren = {}
    for std, cands in col_map.items():
        found = find_col(df, cands)
        if found and found != std:
            ren[found] = std
    df.rename(columns=ren, inplace=True)

    # Duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    if before - len(df):
        log.append(("ok", f"Removed {before - len(df)} duplicate rows"))

    # Date parsing
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    bad = df["Date"].isna().sum()
    if bad:
        log.append(("warn", f"{bad} rows had unparseable dates and were removed"))
        df.dropna(subset=["Date"], inplace=True)

    # String normalisation
    for c in ["DistributorCode", "DistributorName", "SRCode", "StoreID"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.upper()

    if "SRName" not in df.columns:
        df["SRName"] = df["SRCode"]
        log.append(("warn", "SRName column not found -- used SRCode as display name"))
    else:
        df["SRName"] = df["SRName"].astype(str).str.strip().str.title()

    if "DistributorName" not in df.columns:
        df["DistributorName"] = df.get("DistributorCode", pd.Series("UNKNOWN", index=df.index))

    if "PlannedCalls" not in df.columns:
        df["PlannedCalls"] = df.groupby(["SRCode", "Date"])["StoreID"].transform("count")
        log.append(("warn", "PlannedCalls column not found -- derived from store count per SR per day"))
    else:
        df["PlannedCalls"] = pd.to_numeric(df["PlannedCalls"], errors="coerce").fillna(0).astype(int)

    # Drop rows missing mandatory fields
    before = len(df)
    df.dropna(subset=["SRCode", "Date", "StoreID"], inplace=True)
    if before - len(df):
        log.append(("ok", f"Removed {before - len(df)} rows with missing key fields"))

    # Derived time columns
    df["Month"]     = df["Date"].dt.to_period("M").astype(str)
    df["Week"]      = df["Date"].dt.isocalendar().week.astype(int)
    df["DayOfWeek"] = df["Date"].dt.day_name()

    log.insert(0, ("ok", f"Planned dataset: {len(df):,} clean rows ready for analysis"))
    return df, log


# ---------------------------------------------------------------------------
# PREPROCESS -- ACTUAL VISITS
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Preprocessing actual visits...")
def preprocess_actual(raw):
    df = raw.copy()
    df.columns = df.columns.str.strip()
    log = []

    col_map = {
        "DistributorCode": ["DistributorCode", "Distributor Code", "dist_code", "DistCode"],
        "DistributorName": ["DistributorName", "Distributor Name", "dist_name", "Distributor"],
        "SRCode":          ["SRCode", "SR Code", "sr_code", "SalesRepCode", "SR"],
        "SRName":          ["SRName", "SR Name", "sr_name", "SalesRepName", "RepName"],
        "Date":            ["Date", "date", "Visit Date", "VisitDate"],
        "TimeIn":          ["TimeIn", "Time In", "time_in", "CheckIn", "check_in", "timein"],
        "TimeOut":         ["TimeOut", "Time Out", "time_out", "CheckOut", "check_out", "timeout"],
        "CallDuration":    ["CallDuration", "Call Duration", "call_duration", "Duration", "DurationMin"],
        "StoreID":         ["StoreID", "Store ID", "store_id", "Store", "ShopID"],
        "VisitStatus":     ["VisitStatus", "Visit Status", "visit_status", "Status", "CallStatus"],
        "TotalCalls":      ["TotalCalls", "Total Calls", "total_calls", "TotalVisits"],
        "VisitLat":        ["VisitLat", "Visit Lat", "visit_lat", "Latitude", "lat", "Lat", "VisitLatitude"],
        "VisitLon":        ["VisitLon", "Visit Lon", "visit_lon", "Longitude", "lon", "Lon", "Long", "VisitLongitude"],
        "StoreLat":        ["StoreLat", "Store Lat", "store_lat", "StoreLatitude"],
        "StoreLon":        ["StoreLon", "Store Lon", "store_lon", "StoreLongitude"],
    }
    ren = {}
    for std, cands in col_map.items():
        found = find_col(df, cands)
        if found and found != std:
            ren[found] = std
    df.rename(columns=ren, inplace=True)

    # Duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    if before - len(df):
        log.append(("ok", f"Removed {before - len(df)} duplicate rows"))

    # Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    bad = df["Date"].isna().sum()
    if bad:
        log.append(("warn", f"{bad} rows had unparseable dates and were removed"))
        df.dropna(subset=["Date"], inplace=True)

    # TimeIn / TimeOut
    for col in ["TimeIn", "TimeOut"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        else:
            df[col] = pd.NaT
            log.append(("warn", f"{col} column not found -- timestamps set to missing"))

    # CallDuration
    if "CallDuration" not in df.columns:
        if df["TimeIn"].notna().any() and df["TimeOut"].notna().any():
            df["CallDuration"] = (
                (df["TimeOut"] - df["TimeIn"]).dt.total_seconds() / 60
            ).clip(0, 240).round(0)
            log.append(("ok", "CallDuration derived from TimeOut minus TimeIn"))
        else:
            df["CallDuration"] = 20
            log.append(("warn", "CallDuration not found -- defaulted to 20 minutes"))
    else:
        df["CallDuration"] = pd.to_numeric(df["CallDuration"], errors="coerce").fillna(20).astype(int)

    # Fill missing TimeIn from Date, missing TimeOut from TimeIn + duration
    mask_ti = df["TimeIn"].isna() & df["Date"].notna()
    df.loc[mask_ti, "TimeIn"] = df.loc[mask_ti, "Date"] + pd.Timedelta(hours=9)
    mask_to = df["TimeOut"].isna()
    df.loc[mask_to, "TimeOut"] = (
        df.loc[mask_to, "TimeIn"]
        + pd.to_timedelta(df.loc[mask_to, "CallDuration"], unit="m")
    )

    # String normalisation
    for c in ["DistributorCode", "DistributorName", "SRCode", "StoreID"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.upper()

    if "DistributorName" not in df.columns:
        df["DistributorName"] = df.get("DistributorCode", pd.Series("UNKNOWN", index=df.index))

    if "SRName" not in df.columns:
        df["SRName"] = df["SRCode"]
        log.append(("warn", "SRName not found -- used SRCode as display name"))
    else:
        df["SRName"] = df["SRName"].astype(str).str.strip().str.title()

    # VisitStatus
    if "VisitStatus" not in df.columns:
        df["VisitStatus"] = "Successful"
        log.append(("warn", "VisitStatus not found -- defaulted to Successful"))
    else:
        df["VisitStatus"] = df["VisitStatus"].astype(str).str.strip().str.title()
        valid    = {"Successful", "Partial", "Failed"}
        bad_mask = ~df["VisitStatus"].isin(valid)
        if bad_mask.any():
            log.append(("warn", f"{bad_mask.sum()} unrecognised VisitStatus values set to Successful"))
            df.loc[bad_mask, "VisitStatus"] = "Successful"

    # TotalCalls
    if "TotalCalls" not in df.columns:
        df["TotalCalls"] = df.groupby(["SRCode", "Date"])["StoreID"].transform("count")
        log.append(("ok", "TotalCalls derived from visit count per SR per day"))
    else:
        df["TotalCalls"] = pd.to_numeric(df["TotalCalls"], errors="coerce").fillna(1).astype(int)

    # GPS -- fill NaN with approximate values so map pages don't crash
    np.random.seed(0)
    base_lat, base_lon = 10.85, 76.27
    for gc, base in [("VisitLat", base_lat), ("VisitLon", base_lon),
                     ("StoreLat", base_lat),  ("StoreLon", base_lon)]:
        if gc not in df.columns:
            df[gc] = np.nan
        mask_nan = df[gc].isna()
        if mask_nan.any():
            df.loc[mask_nan, gc] = base + np.random.uniform(-0.15, 0.15, mask_nan.sum())
            log.append(("warn", f"{gc} had missing values -- approximated for map display"))

    # Drop rows missing mandatory fields
    before = len(df)
    df.dropna(subset=["SRCode", "Date", "StoreID"], inplace=True)
    if before - len(df):
        log.append(("ok", f"Removed {before - len(df)} rows with missing key fields"))

    # Product sales columns -- detect and standardise
    PRODUCTS = ["Parachute", "Saffola", "TrueElements", "CocoSoul", "Livon"]
    for prod in PRODUCTS:
        candidates = [prod, prod.lower(), prod.upper()]
        found = find_col(df, candidates)
        if found and found != prod:
            df.rename(columns={found: prod}, inplace=True)
        if prod not in df.columns:
            df[prod] = 0
            log.append(("warn", f"Product column '{prod}' not found -- set to 0"))
        else:
            df[prod] = pd.to_numeric(df[prod], errors="coerce").fillna(0).astype(int)
    log.append(("ok", f"Product columns ready: {', '.join(PRODUCTS)}"))
    df["TotalSalesQty"] = df[PRODUCTS].sum(axis=1)

    # Derived columns
    df["Month"]     = df["Date"].dt.to_period("M").astype(str)
    df["Week"]      = df["Date"].dt.isocalendar().week.astype(int)
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Hour"]      = df["TimeIn"].dt.hour.fillna(9).astype(int)

    log.insert(0, ("ok", f"Actual dataset: {len(df):,} clean rows ready for analysis"))
    return df, log


# ---------------------------------------------------------------------------
# PAGE LIST  --  single source of truth for ordering
# ---------------------------------------------------------------------------
PAGES = [
    "Overview",
    "Planned vs Actual",
    "SR Behavior Analysis",
    "Visit Success Analysis",
    "Churn and Risk Analysis",
    "Geographic Insights",
    "Product Analysis",
    "SR vs Product Performance",
    "Preprocessing Report",
]

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
for _k in ["planned_df", "actual_df", "planned_log", "actual_log"]:
    if _k not in st.session_state:
        st.session_state[_k] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    # -- Brand header --
    st.markdown(
        '<div style="text-align:center;padding:22px 0 18px;">'
        '<div style="font-size:18px;font-weight:900;color:#fff;letter-spacing:0.06em;">'
        "SR ANALYTICS</div>"
        '<div style="font-size:11px;font-weight:600;color:#64748b;margin-top:5px;'
        'letter-spacing:0.05em;text-transform:uppercase;">Performance Dashboard</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # -- Upload section header --
    st.markdown(
        '<div style="font-size:10px;font-weight:900;color:#94a3b8;'
        'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;'
        'padding-left:2px;">Step 1 -- Upload Your Data</div>',
        unsafe_allow_html=True,
    )

    planned_file = st.file_uploader(
        "Planned Visits File",
        type=["csv", "xlsx", "xls"],
        key="pu",
        help="Upload the file containing planned visit schedules. Accepts CSV or Excel.",
    )
    actual_file = st.file_uploader(
        "Actual Visits File",
        type=["csv", "xlsx", "xls"],
        key="au",
        help="Upload the file containing actual visit records with timestamps and status.",
    )

    if planned_file:
        try:
            raw = read_file(planned_file)
            st.session_state["planned_df"], st.session_state["planned_log"] = preprocess_planned(raw)
            n = len(st.session_state["planned_df"])
            st.success(f"Planned file loaded -- {n:,} rows ready")
        except Exception as exc:
            st.error(f"Could not load planned file:\n{exc}")

    if actual_file:
        try:
            raw = read_file(actual_file)
            st.session_state["actual_df"], st.session_state["actual_log"] = preprocess_actual(raw)
            n = len(st.session_state["actual_df"])
            st.success(f"Actual file loaded -- {n:,} rows ready")
        except Exception as exc:
            st.error(f"Could not load actual file:\n{exc}")

    data_ready = (
        st.session_state["planned_df"] is not None
        and st.session_state["actual_df"] is not None
    )

    if data_ready:
        st.markdown("---")

        # -- Filter section header --
        st.markdown(
            '<div style="font-size:10px;font-weight:900;color:#94a3b8;'
            'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;'
            'padding-left:2px;">Step 2 -- Filter Data</div>',
            unsafe_allow_html=True,
        )
        p_all = st.session_state["planned_df"]

        dist_opts  = ["All"] + sorted(p_all["DistributorName"].dropna().unique().tolist())
        sel_dist   = st.selectbox(
            "Distributor",
            dist_opts,
            help="Filter all charts to show only this distributor's data.",
        )
        sr_opts    = ["All"] + sorted(p_all["SRCode"].dropna().unique().tolist())
        sel_sr     = st.selectbox(
            "Sales Representative",
            sr_opts,
            help="Filter all charts to show only this SR's data.",
        )
        months     = sorted(p_all["Month"].dropna().unique().tolist())
        sel_months = st.multiselect(
            "Month(s)",
            months,
            default=months,
            help="Select one or more months to include in the analysis.",
        )

        st.markdown("---")

        # -- Date range info --
        d_min = p_all["Date"].min().strftime("%d %b %Y")
        d_max = p_all["Date"].max().strftime("%d %b %Y")
        st.markdown(
            '<div style="font-size:10px;font-weight:700;color:#64748b;'
            f'letter-spacing:0.03em;">Data covers {d_min} to {d_max}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # -- Page indicator in sidebar --
        st.markdown(
            '<div style="font-size:10px;font-weight:900;color:#94a3b8;'
            'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;'
            'padding-left:2px;">Pages</div>',
            unsafe_allow_html=True,
        )
        cur = st.session_state["current_page"]
        for i, pg_name in enumerate(PAGES):
            is_active = i == cur
            bg    = "#1d4ed8" if is_active else "rgba(255,255,255,0.06)"
            color = "#ffffff" if is_active else "#94a3b8"
            weight = "900" if is_active else "700"
            border = "2px solid #3b82f6" if is_active else "2px solid transparent"
            if st.button(
                pg_name,
                key=f"sb_page_{i}",
                use_container_width=True,
            ):
                st.session_state["current_page"] = i
                st.rerun()
            # Style the button via markdown overlay trick -- use CSS nth-child targeting
        page = PAGES[cur]
    else:
        page = None


# ---------------------------------------------------------------------------
# LANDING PAGE  --  shown when no data uploaded yet
# ---------------------------------------------------------------------------
if not data_ready:
    st.markdown(
        '<div style="text-align:center;padding:50px 0 24px;">'
        '<div style="font-size:13px;font-weight:800;color:#1d4ed8;letter-spacing:0.12em;'
        'text-transform:uppercase;margin-bottom:12px;">Sales Force Intelligence</div>'
        '<div style="font-size:30px;font-weight:900;color:#0f172a;letter-spacing:-0.01em;'
        'line-height:1.2;margin-bottom:14px;">'
        "SR Performance Analytics Dashboard</div>"
        '<div style="font-size:14px;font-weight:700;color:#475569;'
        "max-width:560px;margin:0 auto;line-height:1.7;\">"
        "Transform your raw visit data into clear, actionable insights. "
        "Upload your two data files to get started."
        "</div></div>",
        unsafe_allow_html=True,
    )

    _cl, _cm, _cr = st.columns([1, 2, 1])
    with _cm:
        st.markdown(
            '<div class="up-panel">'
            '<div style="font-size:32px;margin-bottom:12px;color:#1d4ed8;font-weight:900;">'
            "Get Started</div>"
            '<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:6px;">'
            "Use the sidebar on the left to upload your files.</div>"
            '<div style="font-size:13px;font-weight:700;color:#64748b;line-height:1.6;">'
            "1. Upload your Planned Visits file<br>"
            "2. Upload your Actual Visits file<br>"
            "3. Use the filters and navigate between pages"
            "</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    def _col_card(title, color, rows):
        items = "".join(
            f'<div style="margin-bottom:6px;"><b>{r[0]}</b> -- {r[1]}</div>'
            for r in rows
        )
        return (
            f'<div class="col-table" style="border-top:4px solid {color};">'
            f'<div style="font-size:15px;font-weight:900;color:{color};margin-bottom:14px;">'
            f"{title}</div>"
            f'<div style="font-size:13px;font-weight:700;color:#000;line-height:1.9;">'
            f"{items}</div>"
            '<div style="margin-top:14px;font-size:11px;font-weight:700;color:#6b7280;">'
            "Accepts CSV, XLSX, XLS -- any encoding is handled automatically</div></div>"
        )

    with c1:
        st.markdown(
            _col_card(
                "PLANNED VISITS FILE", "#1d4ed8",
                [
                    ("DistributorCode", "Distributor identifier"),
                    ("DistributorName", "Distributor full name"),
                    ("SRCode",          "Sales rep code (required)"),
                    ("SRName",          "Sales rep name (optional)"),
                    ("Date",            "Planned visit date (required)"),
                    ("StoreID",         "Target store ID (required)"),
                    ("PlannedCalls",    "Planned calls count (optional)"),
                ],
            ),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            _col_card(
                "ACTUAL VISITS FILE", "#15803d",
                [
                    ("DistributorCode / Name", "Distributor identifiers"),
                    ("SRCode (required)",       "Sales rep code"),
                    ("SRName (optional)",       "Sales rep name"),
                    ("Date (required)",         "Actual visit date"),
                    ("TimeIn / TimeOut",        "Check-in and check-out timestamps"),
                    ("CallDuration",            "Duration in minutes"),
                    ("VisitStatus",             "Successful / Partial / Failed"),
                    ("TotalCalls",              "Total calls made that day"),
                    ("VisitLat / VisitLon",     "GPS coordinates (optional)"),
                    ("StoreLat / StoreLon",     "Store GPS coordinates (optional)"),
                ],
            ),
            unsafe_allow_html=True,
        )

    st.stop()


# ---------------------------------------------------------------------------
# FILTER APPLICATION  --  no copy(), pure boolean indexing for speed
# ---------------------------------------------------------------------------
def filt(df):
    mask = pd.Series(True, index=df.index)
    if sel_dist != "All" and "DistributorName" in df.columns:
        mask &= df["DistributorName"] == sel_dist
    if sel_sr != "All" and "SRCode" in df.columns:
        mask &= df["SRCode"] == sel_sr
    if sel_months and "Month" in df.columns:
        mask &= df["Month"].isin(sel_months)
    return df[mask]


p = filt(st.session_state["planned_df"])
a = filt(st.session_state["actual_df"])


# ---------------------------------------------------------------------------
# PRE-COMPUTE ALL HEAVY AGGREGATIONS ONCE AND CACHE THEM
# These run only when the filtered data actually changes (cache key = data hash)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def compute_sr_perf(p_hash, a_hash, planned_bytes, actual_bytes):
    """SR-level execution + success metrics."""
    sp = p.groupby("SRCode").size().reset_index(name="Planned")
    sa = a.groupby("SRCode").size().reset_index(name="Actual")
    sr = sp.merge(sa, on="SRCode", how="left").fillna(0)
    nm = st.session_state["planned_df"][["SRCode", "SRName"]].drop_duplicates()
    sr = sr.merge(nm, on="SRCode", how="left")
    sr["ExecRate"] = (sr["Actual"] / sr["Planned"].replace(0, np.nan) * 100).fillna(0).clip(0, 150).round(1)
    # Faster than groupby().apply() with lambda
    success_map = (
        a[a["VisitStatus"] == "Successful"]
        .groupby("SRCode").size()
        .reindex(sr["SRCode"]).fillna(0).values
    )
    sr["SuccessCount"] = success_map
    sr["SuccessRate"] = (sr["SuccessCount"] / sr["Actual"].replace(0, np.nan) * 100).fillna(0).round(1)
    sr["Rank"]   = sr["ExecRate"].rank(ascending=False).astype(int)
    sr["Status"] = sr["ExecRate"].apply(lambda x: "High" if x >= 80 else "Medium" if x >= 60 else "Low")
    return sr


@st.cache_data(show_spinner=False)
def compute_monthly(p_hash, a_hash, planned_bytes, actual_bytes):
    mp = p.groupby("Month").size().reset_index(name="Planned")
    ma = a.groupby("Month").agg(
        Actual    =("StoreID",     "count"),
        Successful=("VisitStatus", lambda x: (x == "Successful").sum()),
    ).reset_index()
    return mp.merge(ma, on="Month", how="outer").fillna(0).sort_values("Month")


@st.cache_data(show_spinner=False)
def compute_dist_gap(p_hash, a_hash, planned_bytes, actual_bytes):
    dp = p.groupby("DistributorName").size().reset_index(name="Planned")
    da = a.groupby("DistributorName").size().reset_index(name="Actual")
    return dp.merge(da, on="DistributorName", how="left").fillna(0)


@st.cache_data(show_spinner=False)
def compute_weekly(p_hash, a_hash, planned_bytes, actual_bytes):
    wp = p.groupby("Week").size().reset_index(name="Planned")
    wa = a.groupby("Week").size().reset_index(name="Actual")
    wk = wp.merge(wa, on="Week", how="outer").fillna(0).sort_values("Week")
    wk["Gap"] = (wk["Planned"] - wk["Actual"]).clip(0)
    return wk


@st.cache_data(show_spinner=False)
def compute_status_pct(a_hash, actual_bytes):
    ss  = a.groupby(["SRCode", "VisitStatus"]).size().reset_index(name="Count")
    tot = a.groupby("SRCode").size().reset_index(name="Total")
    ss  = ss.merge(tot, on="SRCode")
    ss["Rate"] = (ss["Count"] / ss["Total"] * 100).round(1)
    return ss


@st.cache_data(show_spinner=False)
def compute_monthly_success(a_hash, actual_bytes):
    ms = a.groupby(["Month", "VisitStatus"]).size().reset_index(name="Count")
    mt = a.groupby("Month").size().reset_index(name="Total")
    ms = ms.merge(mt, on="Month")
    ms["Rate"] = (ms["Count"] / ms["Total"] * 100).round(1)
    return ms[ms["VisitStatus"] == "Successful"].sort_values("Month")


@st.cache_data(show_spinner=False)
def compute_risk(p_hash, a_hash, planned_bytes, actual_bytes):
    sm = a.groupby("SRCode").agg(
        AvgDuration    =("CallDuration", "mean"),
        TotalActual    =("StoreID",      "count"),
        SuccessCount   =("VisitStatus",  lambda x: (x == "Successful").sum()),
        FailCount      =("VisitStatus",  lambda x: (x == "Failed").sum()),
        UniqueStores   =("StoreID",      "nunique"),
        AvgDailyVisits =("TotalCalls",   "mean"),
    ).reset_index()
    sp2 = p.groupby("SRCode").size().reset_index(name="TotalPlanned")
    sm  = sm.merge(sp2, on="SRCode", how="left").fillna(0)
    sm["ExecRate"]    = (sm["TotalActual"] / sm["TotalPlanned"].replace(0, np.nan) * 100).fillna(0).clip(0, 100)
    sm["SuccessRate"] = (sm["SuccessCount"] / sm["TotalActual"].replace(0, np.nan) * 100).fillna(0)
    sm["FailRate"]    = (sm["FailCount"]    / sm["TotalActual"].replace(0, np.nan) * 100).fillna(0)
    sm["RiskScore"]   = (
        (100 - sm["ExecRate"])      * 0.4
        + (100 - sm["SuccessRate"]) * 0.3
        + sm["FailRate"]            * 0.3
    ).round(1)
    sm["RiskLevel"] = sm["RiskScore"].apply(
        lambda x: "High Risk" if x > 55 else "Medium Risk" if x > 35 else "Low Risk"
    )
    nm2 = st.session_state["planned_df"][["SRCode", "SRName"]].drop_duplicates()
    return sm.merge(nm2, on="SRCode", how="left")


@st.cache_data(show_spinner=False)
def compute_scatter_sample(a_hash, actual_bytes):
    """Pre-sample the scatter data so it isn't re-sampled every render."""
    return a.sample(min(2000, len(a)), random_state=42)


@st.cache_data(show_spinner=False)
def compute_heatmap_week(a_hash, actual_bytes):
    hw  = a.groupby(["SRCode", "Week"]).size().reset_index(name="Visits")
    return hw.pivot(index="SRCode", columns="Week", values="Visits").fillna(0)


@st.cache_data(show_spinner=False)
def compute_hour_day_heatmap(a_hash, actual_bytes):
    return a.groupby(["Hour", "DayOfWeek"]).size().reset_index(name="Visits")


@st.cache_data(show_spinner=False)
def compute_dow(a_hash, actual_bytes):
    return a["DayOfWeek"].value_counts().reset_index().rename(columns={"index": "Day", "DayOfWeek": "Visits"})


@st.cache_data(show_spinner=False)
def compute_daily_visits(a_hash, actual_bytes):
    return a.groupby(["SRCode", "Date"]).size().reset_index(name="DailyVisits")


@st.cache_data(show_spinner=False)
def compute_avg_hour(a_hash, actual_bytes):
    ah = a.groupby("SRCode")["Hour"].mean().reset_index()
    ah.columns = ["SRCode", "AvgHour"]
    ah["Label"] = ah["AvgHour"].apply(lambda h: f"{int(h):02d}:{int((h % 1) * 60):02d}")
    return ah


@st.cache_data(show_spinner=False)
def compute_failed_by_dist(a_hash, actual_bytes):
    return (
        a[a["VisitStatus"] == "Failed"]
         .groupby("DistributorName").size()
         .reset_index(name="FailedVisits")
         .sort_values("FailedVisits", ascending=True)
    )


@st.cache_data(show_spinner=False)
def compute_gps_deviation(a_hash, actual_bytes):
    dev = (np.sqrt(
        (a["VisitLat"] - a["StoreLat"]) ** 2
        + (a["VisitLon"] - a["StoreLon"]) ** 2
    ) * 111000).round(0)
    return a.assign(GPSDeviation_m=dev).groupby("SRCode")["GPSDeviation_m"].mean().reset_index(name="AvgDev_m")


PRODUCTS = ["Parachute", "Saffola", "TrueElements", "CocoSoul", "Livon"]
PRODUCT_COLORS = {
    "Parachute":    "#1d4ed8",
    "Saffola":      "#15803d",
    "TrueElements": "#b45309",
    "CocoSoul":     "#6d28d9",
    "Livon":        "#b91c1c",
}


@st.cache_data(show_spinner=False)
def compute_product_totals(a_hash, actual_bytes):
    """Total sales qty per product across all filtered visits."""
    avail = [p for p in PRODUCTS if p in a.columns]
    return a[avail].sum().reset_index().rename(columns={"index": "Product", 0: "TotalQty"})


@st.cache_data(show_spinner=False)
def compute_product_by_sr(a_hash, actual_bytes):
    """Sales qty per SR per product."""
    avail = [p for p in PRODUCTS if p in a.columns]
    return a.groupby("SRCode")[avail].sum().reset_index()


@st.cache_data(show_spinner=False)
def compute_product_monthly(a_hash, actual_bytes):
    """Monthly sales qty per product."""
    avail = [p for p in PRODUCTS if p in a.columns]
    return a.groupby("Month")[avail].sum().reset_index().sort_values("Month")


@st.cache_data(show_spinner=False)
def compute_product_concentration(a_hash, actual_bytes):
    """HHI-based concentration score per SR: 0=balanced, 1=fully concentrated."""
    avail = [p for p in PRODUCTS if p in a.columns]
    by_sr = a.groupby("SRCode")[avail].sum()
    totals = by_sr.sum(axis=1).replace(0, np.nan)
    shares = by_sr.div(totals, axis=0).fillna(0)
    hhi = (shares ** 2).sum(axis=1).round(3)
    result = shares.copy()
    result["HHI"] = hhi
    result["TotalQty"] = by_sr.sum(axis=1).values
    result["DominantProduct"] = by_sr.idxmax(axis=1).values
    result["DominantShare"] = shares.max(axis=1).round(3).values
    return result.reset_index()


@st.cache_data(show_spinner=False)
def compute_sr_product_detail(a_hash, actual_bytes):
    """Per-SR per-product deep metrics: qty, visit count, avg qty per visit,
    success rate, consistency (std of daily sales), month-over-month trend."""
    avail = [p for p in PRODUCTS if p in a.columns]
    rows = []
    srs = sorted(a["SRCode"].unique())
    for sr in srs:
        sub = a[a["SRCode"] == sr]
        total_visits = len(sub)
        succ_visits  = (sub["VisitStatus"] == "Successful").sum()
        for prod in avail:
            prod_sub   = sub[sub[prod] > 0]
            total_qty  = int(sub[prod].sum())
            visit_cnt  = int((sub[prod] > 0).sum())
            avg_per_v  = round(total_qty / visit_cnt, 2) if visit_cnt else 0
            coverage   = round(visit_cnt / total_visits * 100, 1) if total_visits else 0
            # Daily consistency: std of daily sales (lower = more consistent)
            daily = sub.groupby("Date")[prod].sum()
            consistency = round(daily.std(), 2) if len(daily) > 1 else 0.0
            # Month-over-month delta (last month vs first month)
            by_month = sub.groupby("Month")[prod].sum()
            if len(by_month) >= 2:
                mom_delta = int(by_month.iloc[-1] - by_month.iloc[0])
            else:
                mom_delta = 0
            rows.append({
                "SRCode":        sr,
                "Product":       prod,
                "TotalQty":      total_qty,
                "VisitsWithSale": visit_cnt,
                "AvgQtyPerVisit": avg_per_v,
                "CoveragePct":   coverage,
                "Consistency":   consistency,
                "MoMDelta":      mom_delta,
                "SuccessRate":   round(succ_visits / total_visits * 100, 1) if total_visits else 0,
            })
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def compute_sr_monthly_product(a_hash, actual_bytes):
    """Monthly sales per SR per product for trend sparklines."""
    avail = [p for p in PRODUCTS if p in a.columns]
    return (
        a.groupby(["SRCode", "Month"])[avail]
        .sum()
        .reset_index()
        .sort_values(["SRCode", "Month"])
    )


# Build stable cache keys from filter state (lightweight, no full DataFrame hash)
_p_key = (sel_dist, sel_sr, tuple(sel_months), len(p))
_a_key = (sel_dist, sel_sr, tuple(sel_months), len(a))
# Dummy bytes used only as cache-key discriminators (cache_data needs hashable args)
_pb = str(_p_key).encode()
_ab = str(_a_key).encode()


# ===========================================================================
# PAGE: PREPROCESSING REPORT
# ===========================================================================
if page == "Preprocessing Report":
    st.markdown('<div class="pg-title">Data Preprocessing Report</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">A full audit trail of every cleaning and transformation step '
        "applied to your uploaded files. Green badges mean the step completed successfully. "
        "Yellow badges flag assumptions made where data was missing or inconsistent.</div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    for widget, df_key, log_key, label in [
        (c1, "planned_df", "planned_log", "Planned Visits"),
        (c2, "actual_df",  "actual_log",  "Actual Visits"),
    ]:
        with widget:
            section(f"{label} -- Cleaning Log")
            for kind, msg in (st.session_state[log_key] or []):
                cls = "log-ok" if kind == "ok" else "log-warn"
                st.markdown(f'<div class="{cls}">{msg}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            section(f"{label} -- Data Preview (first 10 rows)")
            st.dataframe(
                st.session_state[df_key].head(10),
                use_container_width=True, hide_index=True,
            )

    section("Column Profiles")
    cc1, cc2 = st.columns(2)
    for widget, df_key in [(cc1, "planned_df"), (cc2, "actual_df")]:
        with widget:
            _df = st.session_state[df_key]
            st.dataframe(
                pd.DataFrame({
                    "Column":   _df.columns,
                    "Type":     [str(_df[c].dtype) for c in _df.columns],
                    "Non-Null": [int(_df[c].notna().sum()) for c in _df.columns],
                    "Unique":   [int(_df[c].nunique()) for c in _df.columns],
                }),
                use_container_width=True, hide_index=True,
            )


# ===========================================================================
# PAGE: OVERVIEW
# ===========================================================================
elif page == "Overview":
    st.markdown('<div class="pg-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">A snapshot of the entire operation -- key performance indicators, '
        "execution rates per SR, visit outcomes, and monthly trends. "
        "Start here to understand the big picture before drilling deeper.</div>",
        unsafe_allow_html=True,
    )

    total_planned = len(p)
    total_actual  = len(a)
    exec_rate     = (total_actual / total_planned * 100) if total_planned else 0
    success_rate  = (a["VisitStatus"] == "Successful").sum() / len(a) * 100 if len(a) else 0
    avg_dur       = a["CallDuration"].mean() if len(a) else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Planned Visits", f"{total_planned:,}", color="blue")
    with c2: kpi("Total Actual Visits",  f"{total_actual:,}",  color="green")
    with c3: kpi(
        "Execution Rate", f"{exec_rate:.1f}%",
        delta="Above 80% target" if exec_rate >= 80 else "Below 80% target",
        dir_="up" if exec_rate >= 80 else "down", color="amber",
    )
    with c4: kpi("Overall Success Rate", f"{success_rate:.1f}%", color="purple")
    with c5: kpi("Avg Call Duration",    f"{avg_dur:.0f} min",   color="red")

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Execution rate by SR (cached) --
    section("Execution Rate by Sales Representative")
    sr = compute_sr_perf(_p_key, _a_key, _pb, _ab)
    bar_colors = ["#15803d" if r >= 80 else "#b45309" if r >= 60 else "#b91c1c" for r in sr["ExecRate"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sr["SRCode"], y=sr["ExecRate"], marker_color=bar_colors,
        text=[f"<b>{v:.1f}%</b>" for v in sr["ExecRate"]],
        textposition="outside", textfont=dict(color="#000000", size=12, family="Inter"),
        hovertemplate="<b>%{x}</b><br>Execution Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=80, line_dash="dash", line_color="#1d4ed8", line_width=2,
                  annotation_text="<b>Target: 80%</b>",
                  annotation_font=dict(color="#1d4ed8", size=12, family="Inter"),
                  annotation_position="right")
    sfig(fig, h=370, leg=False)
    fig.update_layout(showlegend=False, yaxis_range=[0, 125])
    fig.update_xaxes(title_text="<b>Sales Representative Code</b>", showgrid=False)
    fig.update_yaxes(title_text="<b>Execution Rate (%)</b>")
    st.plotly_chart(fig, use_container_width=True)
    insight(
        "Each bar shows the percentage of planned visits actually completed by that SR. "
        "<strong>Green = at or above the 80% target, amber = 60-80%, red = below 60%.</strong> "
        "The dashed blue line is the 80% performance benchmark."
    )

    # -- Status donut + monthly trend --
    co1, co2 = st.columns(2)
    with co1:
        section("Visit Status Distribution")
        vc = a["VisitStatus"].value_counts().reset_index()
        vc.columns = ["Status", "Count"]
        cmap = {"Successful": "#15803d", "Partial": "#b45309", "Failed": "#b91c1c"}
        fig2 = px.pie(vc, values="Count", names="Status", color="Status",
                      color_discrete_map=cmap, hole=0.52)
        fig2.update_traces(textinfo="percent+label",
                            textfont=dict(size=13, color="#000000", family="Inter"),
                            pull=[0.02] * len(vc))
        sfig(fig2, h=320)
        st.plotly_chart(fig2, use_container_width=True)
        insight(
            "Donut chart showing what proportion of actual visits were Successful, Partial, or Failed. "
            "<strong>A larger green segment indicates stronger overall execution quality.</strong>"
        )

    with co2:
        section("Monthly Planned vs Actual Trend")
        mt = compute_monthly(_p_key, _a_key, _pb, _ab)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=mt["Month"], y=mt["Planned"], name="<b>Planned</b>",
                                   line=dict(color="#6b7280", dash="dash", width=2.5),
                                   mode="lines+markers", marker=dict(size=7, color="#6b7280")))
        fig3.add_trace(go.Scatter(x=mt["Month"], y=mt["Actual"], name="<b>Actual</b>",
                                   line=dict(color="#1d4ed8", width=3),
                                   fill="tonexty", fillcolor="rgba(29,78,216,0.08)",
                                   mode="lines+markers", marker=dict(size=7, color="#1d4ed8")))
        fig3.add_trace(go.Scatter(x=mt["Month"], y=mt["Successful"], name="<b>Successful</b>",
                                   line=dict(color="#15803d", width=2.5),
                                   mode="lines+markers", marker=dict(size=7, color="#15803d")))
        sfig(fig3, h=320)
        fig3.update_xaxes(title_text="<b>Month</b>", showgrid=False)
        fig3.update_yaxes(title_text="<b>Number of Visits</b>")
        st.plotly_chart(fig3, use_container_width=True)
        insight(
            "Month-over-month trend lines for planned (grey dashed), actual (blue), and successful (green) visits. "
            "<strong>The gap between the grey and blue lines is the missed visits for that month.</strong>"
        )

    # -- Leaderboard --
    section("SR Performance Leaderboard")
    lb = sr.sort_values("ExecRate", ascending=False)[[
        "Rank", "SRCode", "SRName", "Planned", "Actual", "ExecRate", "SuccessRate", "Status"
    ]].rename(columns={
        "ExecRate": "Exec Rate (%)", "SuccessRate": "Success Rate (%)",
        "SRCode": "SR Code", "SRName": "SR Name",
    })
    st.dataframe(lb, use_container_width=True, hide_index=True)
    insight(
        "<strong>Exec Rate = Actual / Planned x 100.</strong> "
        "Success Rate = Successful Visits / Actual Visits x 100. "
        "Click any column header to re-sort the table."
    )


# ===========================================================================
# PAGE: PLANNED VS ACTUAL
# ===========================================================================
elif page == "Planned vs Actual":
    st.markdown('<div class="pg-title">Planned vs Actual Visit Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Compare what was scheduled against what was actually executed. '
        "Identify which distributors, weeks, or days have the largest gaps "
        "so you can prioritise corrective action.</div>",
        unsafe_allow_html=True,
    )

    section("Execution Gap by Distributor")
    dg = compute_dist_gap(_p_key, _a_key, _pb, _ab)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="<b>Planned</b>", x=dg["DistributorName"], y=dg["Planned"],
                         marker_color="#94a3b8", text=dg["Planned"].astype(int),
                         textposition="outside", textfont=dict(color="#000000", size=11, family="Inter")))
    fig.add_trace(go.Bar(name="<b>Actual</b>", x=dg["DistributorName"], y=dg["Actual"],
                         marker_color="#1d4ed8", text=dg["Actual"].astype(int),
                         textposition="outside", textfont=dict(color="#000000", size=11, family="Inter")))
    sfig(fig, h=390)
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="<b>Distributor</b>", showgrid=False)
    fig.update_yaxes(title_text="<b>Number of Visits</b>")
    st.plotly_chart(fig, use_container_width=True)
    insight(
        "Grouped bars compare planned (grey) vs actual (blue) visits per distributor. "
        "<strong>A shorter blue bar relative to grey shows a larger execution gap for that distributor.</strong>"
    )

    co1, co2 = st.columns(2)
    with co1:
        section("SR Activity Heatmap by Week")
        piv = compute_heatmap_week(_a_key, _ab)
        fig2 = px.imshow(piv, color_continuous_scale="Blues", aspect="auto",
                          labels=dict(x="<b>Week Number</b>", y="<b>SR Code</b>", color="<b>Visits</b>"))
        fig2.update_xaxes(title_text="<b>Week Number</b>",
                           title_font=dict(color="#000", family="Inter", size=13))
        fig2.update_yaxes(title_text="<b>SR Code</b>",
                           title_font=dict(color="#000", family="Inter", size=13))
        fig2.update_coloraxes(colorbar=dict(
            tickfont=dict(color="#000", family="Inter", size=11),
            title=dict(text="<b>Visits</b>", font=dict(color="#000", family="Inter")),
        ))
        fig2.update_layout(height=340, paper_bgcolor="white", font=FONT,
                            margin=dict(t=20, b=50, l=60, r=20))
        st.plotly_chart(fig2, use_container_width=True)
        insight(
            "Each cell shows actual visits by one SR in a given week. "
            "<strong>Darker blue means more visits. Pale cells are low-activity weeks worth investigating.</strong>"
        )

    with co2:
        section("Visit Volume by Day of Week")
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dw = compute_dow(_a_key, _ab)
        dw.columns = ["Day", "Visits"]
        dw = dw.set_index("Day").reindex([d for d in dow_order if d in dw["Day"].values]).reset_index()
        fig3 = px.bar(dw, x="Day", y="Visits", color="Visits",
                      color_continuous_scale="RdYlGn",
                      text=[f"<b>{v}</b>" for v in dw["Visits"]],
                      labels={"Day": "<b>Day of Week</b>", "Visits": "<b>Actual Visits</b>"})
        fig3.update_traces(textposition="outside",
                            textfont=dict(color="#000000", size=11, family="Inter"))
        fig3.update_coloraxes(showscale=False)
        sfig(fig3, h=340)
        fig3.update_xaxes(title_text="<b>Day of Week</b>", showgrid=False)
        fig3.update_yaxes(title_text="<b>Actual Visits</b>")
        st.plotly_chart(fig3, use_container_width=True)
        insight(
            "Red bars indicate low-activity days and green bars indicate high-activity days. "
            "<strong>Recurring dips on the same weekday suggest a scheduling pattern that needs review.</strong>"
        )

    section("Weekly Planned vs Actual with Missed Visit Gap")
    wk = compute_weekly(_p_key, _a_key, _pb, _ab)
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=wk["Week"], y=wk["Planned"], name="<b>Planned</b>",
                               line=dict(color="#6b7280", dash="dash", width=2.5),
                               mode="lines+markers"), secondary_y=False)
    fig4.add_trace(go.Scatter(x=wk["Week"], y=wk["Actual"], name="<b>Actual</b>",
                               line=dict(color="#1d4ed8", width=3),
                               fill="tonexty", fillcolor="rgba(29,78,216,0.09)",
                               mode="lines+markers"), secondary_y=False)
    fig4.add_trace(go.Bar(x=wk["Week"], y=wk["Gap"], name="<b>Missed Visits</b>",
                           marker_color="rgba(185,28,28,0.25)",
                           marker_line=dict(color="#b91c1c", width=1.2)), secondary_y=True)
    fig4.update_xaxes(title_text="<b>Week Number</b>", **AXIS)
    fig4.update_yaxes(title_text="<b>Visit Count</b>", secondary_y=False, **AXIS)
    fig4.update_yaxes(title_text="<b>Missed Visits</b>", secondary_y=True, showgrid=False,
                      tickfont=dict(color="#000", family="Inter", size=12),
                      title_font=dict(color="#000", family="Inter", size=13))
    _lay4 = {**LAY, "legend": dict(orientation="h", y=-0.28,
                                    font=dict(color="#000", family="Inter", size=12))}
    fig4.update_layout(height=390, **_lay4)
    st.plotly_chart(fig4, use_container_width=True)
    insight(
        "Lines (left axis) show planned vs actual visit volume each week. "
        "<strong>Red bars (right axis) show the missed visit gap. "
        "Tall red bars in a week signal a high-priority execution failure.</strong>"
    )


# ===========================================================================
# PAGE: SR BEHAVIOR
# ===========================================================================
elif page == "SR Behavior Analysis":
    st.markdown('<div class="pg-title">SR Behavior Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Understand how each SR works in the field -- '
        "when they start their day, how long they spend per visit, "
        "how many calls they make, and which hours are most active. "
        "Use this to coach individuals and optimise scheduling.</div>",
        unsafe_allow_html=True,
    )

    section("Call Duration Distribution by SR")
    fig = px.box(a, x="SRCode", y="CallDuration", color="SRCode",
                 labels={"SRCode": "<b>SR Code</b>", "CallDuration": "<b>Call Duration (Minutes)</b>"},
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_traces(marker=dict(size=4))
    sfig(fig, h=400, leg=False)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
    fig.update_yaxes(title_text="<b>Call Duration (Minutes)</b>")
    st.plotly_chart(fig, use_container_width=True)
    insight(
        "Box plots show the spread of call durations per SR. "
        "<strong>The box covers the middle 50% of visits. The centre line is the median. "
        "Dots are outliers.</strong> Wide boxes indicate inconsistency. "
        "Very low medians may suggest rushed or incomplete visits."
    )

    co1, co2 = st.columns(2)
    with co1:
        section("Average First Visit Start Time by SR")
        ah = compute_avg_hour(_a_key, _ab)
        bc = ["#15803d" if h <= 9.5 else "#b45309" if h <= 10.5 else "#b91c1c" for h in ah["AvgHour"]]
        fig2 = go.Figure(go.Bar(
            x=ah["SRCode"], y=ah["AvgHour"], marker_color=bc,
            text=[f"<b>{l}</b>" for l in ah["Label"]], textposition="outside",
            textfont=dict(color="#000000", size=11, family="Inter"),
        ))
        fig2.add_hline(y=9, line_dash="dash", line_color="#1d4ed8", line_width=2,
                       annotation_text="<b>Target: 9:00 AM</b>",
                       annotation_font=dict(color="#1d4ed8", size=12, family="Inter"),
                       annotation_position="right")
        sfig(fig2, h=350)
        fig2.update_layout(yaxis_range=[7, 14], showlegend=False)
        fig2.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
        fig2.update_yaxes(title_text="<b>Average Start Hour (24h Format)</b>")
        st.plotly_chart(fig2, use_container_width=True)
        insight(
            "Shows the average hour each SR begins their first visit. "
            "<strong>Green = starts by 9:00 AM, amber = slightly late, red = consistently late.</strong> "
            "Late starts compress the available selling window."
        )

    with co2:
        section("Daily Visit Volume Distribution by SR")
        dv = compute_daily_visits(_a_key, _ab)
        fig3 = px.violin(dv, x="SRCode", y="DailyVisits", color="SRCode",
                          box=True, points="outliers",
                          labels={"SRCode": "<b>SR Code</b>", "DailyVisits": "<b>Visits per Day</b>"},
                          color_discrete_sequence=px.colors.qualitative.Bold)
        sfig(fig3, h=350, leg=False)
        fig3.update_layout(showlegend=False)
        fig3.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
        fig3.update_yaxes(title_text="<b>Visits per Day</b>")
        st.plotly_chart(fig3, use_container_width=True)
        insight(
            "Violin plots show the full distribution of daily visit counts per SR. "
            "<strong>Wider shapes at higher visit counts indicate more productive days. "
            "Narrow shapes at low counts indicate consistently low daily output.</strong>"
        )

    section("Activity Heatmap -- Hour of Day vs Day of Week")
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hd = compute_hour_day_heatmap(_a_key, _ab)
    hd["DayOfWeek"] = pd.Categorical(
        hd["DayOfWeek"],
        categories=[d for d in dow_order if d in hd["DayOfWeek"].values],
        ordered=True,
    )
    piv2 = hd.pivot(index="Hour", columns="DayOfWeek", values="Visits").fillna(0)
    fig4 = px.imshow(piv2, color_continuous_scale="YlOrRd", aspect="auto",
                      labels=dict(x="<b>Day of Week</b>", y="<b>Hour of Day (24h)</b>", color="<b>Visits</b>"))
    fig4.update_xaxes(title_text="<b>Day of Week</b>",
                       title_font=dict(color="#000", family="Inter", size=13))
    fig4.update_yaxes(title_text="<b>Hour of Day (24h)</b>",
                       title_font=dict(color="#000", family="Inter", size=13))
    fig4.update_coloraxes(colorbar=dict(
        tickfont=dict(color="#000", family="Inter", size=11),
        title=dict(text="<b>Visits</b>", font=dict(color="#000", family="Inter")),
    ))
    fig4.update_layout(height=400, paper_bgcolor="white", font=FONT,
                        margin=dict(t=20, b=60, l=60, r=20))
    st.plotly_chart(fig4, use_container_width=True)
    insight(
        "Each cell shows the number of visits in that hour-day slot across all SRs. "
        "<strong>Darker red means higher activity. Use this to identify peak selling windows "
        "and flag dead zones where field activity is absent.</strong>"
    )


# ===========================================================================
# PAGE: VISIT SUCCESS
# ===========================================================================
elif page == "Visit Success Analysis":
    st.markdown('<div class="pg-title">Visit Success and Failure Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Break down visit outcomes into Successful, Partial, and Failed categories. '
        "Spot trends over time and identify which distributors or SRs have the highest failure rates "
        "so management can intervene early.</div>",
        unsafe_allow_html=True,
    )

    section("Visit Outcome Breakdown by SR")
    ss = compute_status_pct(_a_key, _ab)
    fig = px.bar(ss, x="SRCode", y="Rate", color="VisitStatus", barmode="stack",
                 color_discrete_map={"Successful": "#15803d", "Partial": "#b45309", "Failed": "#b91c1c"},
                 labels={"SRCode": "<b>SR Code</b>", "Rate": "<b>Percentage of Visits (%)</b>",
                          "VisitStatus": "Status"},
                 text_auto=".1f")
    fig.update_traces(textfont=dict(color="#000000", size=11, family="Inter"))
    sfig(fig, h=390)
    fig.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
    fig.update_yaxes(title_text="<b>Percentage of Visits (%)</b>")
    st.plotly_chart(fig, use_container_width=True)
    insight(
        "Stacked bars show visit outcome proportions per SR as a percentage. "
        "<strong>A taller green section means better execution quality. "
        "Large red or amber sections flag SRs who need coaching or support.</strong>"
    )

    co1, co2 = st.columns(2)
    with co1:
        section("Monthly Success Rate Trend")
        msc = compute_monthly_success(_a_key, _ab)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=msc["Month"], y=msc["Rate"],
            mode="lines+markers+text",
            text=[f"<b>{v:.0f}%</b>" for v in msc["Rate"]],
            textposition="top center",
            textfont=dict(color="#000000", size=11, family="Inter"),
            line=dict(color="#15803d", width=3),
            marker=dict(size=9, color="#15803d"),
            fill="tozeroy", fillcolor="rgba(21,128,61,0.09)",
        ))
        fig2.add_hline(y=70, line_dash="dash", line_color="#b45309", line_width=2,
                       annotation_text="<b>Target: 70%</b>",
                       annotation_font=dict(color="#b45309", size=12, family="Inter"),
                       annotation_position="right")
        sfig(fig2, h=330)
        fig2.update_layout(yaxis_range=[0, 105])
        fig2.update_xaxes(title_text="<b>Month</b>", showgrid=False)
        fig2.update_yaxes(title_text="<b>Success Rate (%)</b>")
        st.plotly_chart(fig2, use_container_width=True)
        insight(
            "Monthly success rate against the 70% quality target (amber dashed line). "
            "<strong>A declining trend is a signal to initiate coaching or a process audit immediately.</strong>"
        )

    with co2:
        section("Failed Visits by Distributor")
        fv = compute_failed_by_dist(_a_key, _ab)
        fig3 = go.Figure(go.Bar(
            y=fv["DistributorName"], x=fv["FailedVisits"], orientation="h",
            marker_color="#b91c1c",
            text=[f"<b>{v}</b>" for v in fv["FailedVisits"]], textposition="outside",
            textfont=dict(color="#000000", size=11, family="Inter"),
        ))
        sfig(fig3, h=330)
        fig3.update_layout(margin=dict(t=20, b=50, l=160, r=40))
        fig3.update_xaxes(title_text="<b>Number of Failed Visits</b>")
        fig3.update_yaxes(title_text="<b>Distributor</b>", showgrid=False)
        st.plotly_chart(fig3, use_container_width=True)
        insight(
            "Longer red bars mean more failed visits under that distributor. "
            "<strong>Investigate whether failures are SR-driven, store-level, "
            "or territory-related to choose the right corrective action.</strong>"
        )

    section("Call Duration vs Total Daily Calls -- Coloured by Visit Status")
    samp = compute_scatter_sample(_a_key, _ab)
    fig4 = px.scatter(
        samp, x="CallDuration", y="TotalCalls", color="VisitStatus",
        color_discrete_map={"Successful": "#15803d", "Partial": "#b45309", "Failed": "#b91c1c"},
        labels={"CallDuration": "<b>Call Duration (Minutes)</b>",
                "TotalCalls":   "<b>Total Calls Made That Day</b>", "VisitStatus": "Status"},
        opacity=0.65,
    )
    sfig(fig4, h=400)
    fig4.update_xaxes(title_text="<b>Call Duration (Minutes)</b>")
    fig4.update_yaxes(title_text="<b>Total Calls Made That Day</b>")
    st.plotly_chart(fig4, use_container_width=True)
    insight(
        "Each dot is one visit. The X axis is call duration and the Y axis is how many "
        "total calls the SR made that day. "
        "<strong>Green dot clusters in a zone reveal the optimal duration and volume "
        "combination that produces successful outcomes.</strong>"
    )


# ===========================================================================
# PAGE: CHURN AND RISK
# ===========================================================================
elif page == "Churn and Risk Analysis":
    st.markdown('<div class="pg-title">Churn Prediction and Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Each SR is scored 0-100 based on execution failure, visit quality, '
        "and fail rate. High-risk SRs are flagged for immediate attention. "
        "Use the quadrant chart to quickly spot who needs support and who is performing well.</div>",
        unsafe_allow_html=True,
    )

    sm = compute_risk(_p_key, _a_key, _pb, _ab)

    co1, co2, co3, co4 = st.columns(4)
    with co1: kpi("High Risk SRs",   str((sm["RiskLevel"] == "High Risk").sum()),   color="red")
    with co2: kpi("Medium Risk SRs", str((sm["RiskLevel"] == "Medium Risk").sum()), color="amber")
    with co3: kpi("Low Risk SRs",    str((sm["RiskLevel"] == "Low Risk").sum()),    color="green")
    with co4: kpi("Avg Risk Score",  f"{sm['RiskScore'].mean():.1f} / 100",         color="purple")
    st.markdown("<br>", unsafe_allow_html=True)

    section("SR Risk Quadrant -- Execution Rate vs Success Rate")
    cmap2 = {"High Risk": "#b91c1c", "Medium Risk": "#b45309", "Low Risk": "#15803d"}
    fig = px.scatter(sm, x="ExecRate", y="SuccessRate",
                     size="RiskScore", color="RiskLevel", color_discrete_map=cmap2,
                     text="SRCode",
                     labels={"ExecRate":    "<b>Execution Rate (%)</b>",
                             "SuccessRate": "<b>Success Rate (%)</b>",
                             "RiskLevel":   "Risk Level"},
                     hover_data=["SRName", "RiskScore"])
    fig.update_traces(textposition="top center",
                      textfont=dict(color="#000000", size=12, family="Inter"))
    fig.add_vline(x=80, line_dash="dash", line_color="#475569", line_width=1.5,
                  annotation_text="<b>Exec Target 80%</b>",
                  annotation_font=dict(color="#475569", size=11, family="Inter"))
    fig.add_hline(y=70, line_dash="dash", line_color="#475569", line_width=1.5,
                  annotation_text="<b>Success Target 70%</b>",
                  annotation_font=dict(color="#475569", size=11, family="Inter"))
    for label, xp, yp, bg, tc in [
        ("Champions",         92, 88, "#d1fae5", "#166534"),
        ("At Risk",           25, 15, "#fee2e2", "#991b1b"),
        ("Low Execution",     25, 88, "#fef9c3", "#854d0e"),
        ("High Vol / Low Q",  88, 15, "#fef3c7", "#92400e"),
    ]:
        fig.add_annotation(x=xp, y=yp, text=f"<b>{label}</b>", showarrow=False,
                            font=dict(size=10, color=tc, family="Inter"),
                            bgcolor=bg, borderpad=5, opacity=0.9)
    sfig(fig, h=460)
    fig.update_xaxes(title_text="<b>Execution Rate (% of Planned Visits Completed)</b>", range=[0, 110])
    fig.update_yaxes(title_text="<b>Success Rate (% of Actual Visits Successful)</b>",   range=[0, 110])
    st.plotly_chart(fig, use_container_width=True)
    insight(
        "Each bubble is an SR. X axis is execution rate, Y axis is success rate, "
        "and bubble size is risk score. "
        "<strong>Top-right quadrant is Champions. Bottom-left is At Risk. "
        "Dashed lines mark the performance targets.</strong>"
    )

    section("SR Risk Score Ranking")
    disp = sm.sort_values("RiskScore", ascending=False)[[
        "SRCode", "SRName", "ExecRate", "SuccessRate", "FailRate", "RiskScore", "RiskLevel"
    ]].copy()
    for _c in ["ExecRate", "SuccessRate", "FailRate"]:
        disp[_c] = disp[_c].round(1).astype(str) + "%"
    st.dataframe(
        disp.rename(columns={"SRCode": "SR Code", "SRName": "SR Name", "ExecRate": "Exec Rate",
                               "SuccessRate": "Success Rate", "FailRate": "Fail Rate",
                               "RiskScore": "Risk Score (0-100)", "RiskLevel": "Risk Level"}),
        use_container_width=True, hide_index=True,
    )
    insight(
        "<strong>Risk Score combines:</strong> execution failure rate (40%), poor success rate (30%), "
        "and fail rate (30%). Scores above 55 are High Risk, 35-55 are Medium Risk, "
        "and below 35 are Low Risk."
    )

    section("Multi-Dimensional Performance Radar")
    cats = ["Exec Rate", "Success Rate", "Avg Duration", "Daily Visits", "Store Coverage"]
    clrs = px.colors.qualitative.Bold
    fig2 = go.Figure()
    mx_dv = max(sm["AvgDailyVisits"].max(), 1)
    mx_st = max(sm["UniqueStores"].max(), 1)
    for i, row in sm.iterrows():
        vals = [
            min(row["ExecRate"], 100),
            min(row["SuccessRate"], 100),
            min(row["AvgDuration"] / 60 * 100, 100),
            min(row["AvgDailyVisits"] / mx_dv * 100, 100),
            min(row["UniqueStores"] / mx_st * 100, 100),
        ]
        fig2.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", name=f"<b>{row['SRCode']}</b>",
            line_color=clrs[i % len(clrs)], opacity=0.75,
        ))
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100],
                             tickfont=dict(color="#000000", family="Inter", size=11)),
            angularaxis=dict(tickfont=dict(color="#000000", family="Inter", size=12)),
        ),
        height=440, paper_bgcolor="white", font=FONT,
        legend=dict(orientation="h", y=-0.12,
                     font=dict(color="#000000", family="Inter", size=11)),
        margin=dict(t=30, b=60, l=60, r=60),
    )
    st.plotly_chart(fig2, use_container_width=True)
    insight(
        "Each polygon represents one SR across five performance dimensions. "
        "<strong>A larger and fuller polygon indicates a stronger overall performer. "
        "Small or lopsided shapes identify specific weaknesses to target with coaching.</strong>"
    )


# ===========================================================================
# PAGE: GEOGRAPHIC
# ===========================================================================
elif page == "Geographic Insights":
    st.markdown('<div class="pg-title">Geographic Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Visualise where visits happen on a map, identify territory gaps, '
        "and detect GPS deviation anomalies that may indicate check-in irregularities. "
        "Requires VisitLat and VisitLon columns in your Actual Visits file.</div>",
        unsafe_allow_html=True,
    )

    valid_gps = a[a["VisitLat"].notna() & a["VisitLon"].notna()]
    if len(valid_gps) < 10:
        st.warning(
            "Insufficient GPS data found. Geographic maps require VisitLat and VisitLon "
            "columns with real coordinate values."
        )
    else:
        section("Visit Location Density Map")
        sg = valid_gps.sample(min(3000, len(valid_gps)), random_state=42)
        fig = px.density_mapbox(
            sg, lat="VisitLat", lon="VisitLon", z="CallDuration", radius=14,
            center=dict(lat=sg["VisitLat"].mean(), lon=sg["VisitLon"].mean()),
            zoom=9, mapbox_style="open-street-map", color_continuous_scale="YlOrRd",
            labels={"CallDuration": "<b>Duration (min)</b>"},
            hover_data=["SRCode", "VisitStatus"],
        )
        fig.update_layout(height=480, margin=dict(t=10, b=10, l=10, r=10), font=FONT,
                           coloraxis_colorbar=dict(
                               tickfont=dict(color="#000", family="Inter"),
                               title=dict(text="<b>Duration</b>",
                                          font=dict(color="#000", family="Inter"))))
        st.plotly_chart(fig, use_container_width=True)
        insight(
            "Colour intensity shows visit density. "
            "<strong>Hotter red zones have high visit concentration. "
            "Sparse areas may indicate under-served territories or routing inefficiencies.</strong>"
        )

        co1, co2 = st.columns(2)
        with co1:
            section("Visit Outcome Map")
            ss2 = valid_gps.sample(min(1500, len(valid_gps)), random_state=99)
            fig2 = px.scatter_mapbox(
                ss2, lat="VisitLat", lon="VisitLon", color="VisitStatus",
                color_discrete_map={"Successful": "#15803d", "Partial": "#b45309", "Failed": "#b91c1c"},
                size_max=9, zoom=9, mapbox_style="open-street-map",
                center=dict(lat=ss2["VisitLat"].mean(), lon=ss2["VisitLon"].mean()),
                hover_data=["SRCode", "CallDuration"],
            )
            fig2.update_layout(height=400, margin=dict(t=10, b=10, l=10, r=10), font=FONT)
            st.plotly_chart(fig2, use_container_width=True)
            insight(
                "Green dots are successful visits, amber are partial, and red are failed. "
                "<strong>Clusters of red in a zone indicate a problem territory "
                "that needs targeted investigation or additional support.</strong>"
            )

        with co2:
            section("SR Territory Coverage")
            sg2 = a.groupby("SRCode").agg(
                CenterLat   =("VisitLat", "mean"),
                CenterLon   =("VisitLon", "mean"),
                TotalVisits =("StoreID",  "count"),
                UniqueStores=("StoreID",  "nunique"),
            ).reset_index()
            fig3 = px.scatter_mapbox(
                sg2, lat="CenterLat", lon="CenterLon",
                size="TotalVisits", color="UniqueStores", text="SRCode",
                zoom=9, mapbox_style="open-street-map",
                center=dict(lat=sg2["CenterLat"].mean(), lon=sg2["CenterLon"].mean()),
                color_continuous_scale="Blues",
                labels={"UniqueStores": "<b>Unique Stores</b>", "TotalVisits": "<b>Total Visits</b>"},
            )
            fig3.update_layout(height=400, margin=dict(t=10, b=10, l=10, r=10), font=FONT)
            st.plotly_chart(fig3, use_container_width=True)
            insight(
                "Each bubble is an SR's activity centroid. "
                "<strong>Bubble size is total visits and blue depth is unique store coverage. "
                "Overlapping centres suggest territorial redundancy. Gaps suggest under-covered areas.</strong>"
            )

        section("GPS Deviation: SR Check-In Location vs Registered Store Location")
        gd = compute_gps_deviation(_a_key, _ab)
        bc2 = ["#b91c1c" if v > 500 else "#b45309" if v > 200 else "#15803d" for v in gd["AvgDev_m"]]
        fig4 = go.Figure(go.Bar(
            x=gd["SRCode"], y=gd["AvgDev_m"], marker_color=bc2,
            text=[f"<b>{v:.0f}m</b>" for v in gd["AvgDev_m"]], textposition="outside",
            textfont=dict(color="#000000", size=11, family="Inter"),
        ))
        fig4.add_hline(y=300, line_dash="dash", line_color="#1d4ed8", line_width=2,
                       annotation_text="<b>Acceptable Threshold: 300m</b>",
                       annotation_font=dict(color="#1d4ed8", size=12, family="Inter"),
                       annotation_position="right")
        sfig(fig4, h=360)
        fig4.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
        fig4.update_yaxes(title_text="<b>Average GPS Deviation (Metres)</b>")
        st.plotly_chart(fig4, use_container_width=True)
        insight(
            "GPS deviation is the distance between where the SR checked in and "
            "the store's registered GPS coordinates. "
            "<strong>Values above 300 metres may indicate check-in fraud, navigation errors, "
            "or data quality issues that require follow-up.</strong>"
        )

# ===========================================================================
# PAGE: PRODUCT ANALYSIS
# ===========================================================================
elif page == "Product Analysis":
    st.markdown('<div class="pg-title">Product Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Understand which products drive revenue, which SRs have concentrated '
        "portfolios, and where sales opportunities remain untapped across Parachute, Saffola, "
        "TrueElements, CocoSoul, and Livon.</div>",
        unsafe_allow_html=True,
    )

    avail_products = [p for p in PRODUCTS if p in a.columns]

    if not avail_products:
        st.warning(
            "No product sales columns found in your Actual Visits dataset. "
            "Please ensure your file contains columns named: "
            + ", ".join(PRODUCTS)
        )
    else:
        # -- KPI row ---------------------------------------------------------
        prod_totals = compute_product_totals(_a_key, _ab)
        total_all   = int(prod_totals["TotalQty"].sum())
        top_product = prod_totals.loc[prod_totals["TotalQty"].idxmax(), "Product"]
        top_qty     = int(prod_totals["TotalQty"].max())
        top_share   = round(top_qty / total_all * 100, 1) if total_all else 0
        low_products = prod_totals[prod_totals["TotalQty"] < prod_totals["TotalQty"].mean() * 0.4]
        n_low        = len(low_products)

        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi("Total Units Sold", f"{total_all:,}", color="blue")
        with c2: kpi("Top Product", top_product, delta=f"{top_share}% of all sales", dir_="up", color="green")
        with c3: kpi("Products Tracked", str(len(avail_products)), color="purple")
        with c4: kpi("Under-Performed Products", str(n_low), delta="Below avg volume", dir_="down" if n_low else "up", color="amber")

        st.markdown("<br>", unsafe_allow_html=True)

        # -- Overall product distribution -------------------------------------
        section("Overall Product Sales Distribution")
        co1, co2 = st.columns(2)

        with co1:
            colors_list = [PRODUCT_COLORS.get(p, "#64748b") for p in prod_totals["Product"]]
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=prod_totals["Product"],
                y=prod_totals["TotalQty"],
                marker_color=colors_list,
                text=[f"<b>{int(v):,}</b>" for v in prod_totals["TotalQty"]],
                textposition="outside",
                textfont=dict(color="#000000", size=12, family="Inter"),
                hovertemplate="<b>%{x}</b><br>Units: %{y:,}<extra></extra>",
            ))
            sfig(fig1, h=360, leg=False)
            fig1.update_layout(showlegend=False)
            fig1.update_xaxes(title_text="<b>Product</b>", showgrid=False)
            fig1.update_yaxes(title_text="<b>Total Units Sold</b>")
            st.plotly_chart(fig1, use_container_width=True)

        with co2:
            fig2 = px.pie(
                prod_totals, values="TotalQty", names="Product",
                color="Product",
                color_discrete_map=PRODUCT_COLORS,
                hole=0.50,
            )
            fig2.update_traces(
                textinfo="percent+label",
                textfont=dict(size=13, color="#000000", family="Inter"),
                pull=[0.04 if p in ("CocoSoul","Livon") else 0.01 for p in prod_totals["Product"]],
            )
            sfig(fig2, h=360)
            st.plotly_chart(fig2, use_container_width=True)

        insight(
            "The bar and donut charts show the overall sales volume split. "
            "<strong>Parachute, Saffola, and TrueElements dominate total units sold</strong>, "
            "reflecting their role as primary portfolio products. "
            "CocoSoul and Livon are pulled out slightly in the donut to highlight their lower share -- "
            "these represent expansion opportunities."
        )

        # -- SR product sales heatmap -----------------------------------------
        section("Sales Volume by SR and Product (Heatmap)")
        by_sr = compute_product_by_sr(_a_key, _ab)
        by_sr_melt = by_sr.melt(id_vars="SRCode", value_vars=avail_products,
                                 var_name="Product", value_name="Qty")
        pivot_heat = by_sr.set_index("SRCode")[avail_products]

        fig3 = px.imshow(
            pivot_heat,
            color_continuous_scale="Blues",
            aspect="auto",
            labels=dict(x="<b>Product</b>", y="<b>SR Code</b>", color="<b>Units Sold</b>"),
        )
        fig3.update_xaxes(title_text="<b>Product</b>", title_font=dict(color="#000", family="Inter", size=13))
        fig3.update_yaxes(title_text="<b>SR Code</b>",  title_font=dict(color="#000", family="Inter", size=13))
        fig3.update_coloraxes(colorbar=dict(
            tickfont=dict(color="#000", family="Inter", size=11),
            title=dict(text="<b>Units</b>", font=dict(color="#000", family="Inter")),
        ))
        fig3.update_layout(height=400, paper_bgcolor="white", font=FONT,
                            margin=dict(t=20, b=60, l=60, r=20))
        st.plotly_chart(fig3, use_container_width=True)
        insight(
            "Darker blue = higher sales volume for that SR-product combination. "
            "<strong>Pale or white cells reveal product gaps</strong> -- SRs who barely sell that product. "
            "Rows that are uniformly dark indicate well-rounded SRs; "
            "rows with only one or two dark cells indicate highly concentrated SRs."
        )

        # -- Stacked bar: SR breakdown -----------------------------------------
        section("Product Mix per SR (Stacked by Volume)")
        fig4 = go.Figure()
        for prod in avail_products:
            fig4.add_trace(go.Bar(
                name=f"<b>{prod}</b>",
                x=by_sr["SRCode"],
                y=by_sr[prod],
                marker_color=PRODUCT_COLORS.get(prod, "#64748b"),
                hovertemplate=f"<b>{prod}</b><br>SR: %{{x}}<br>Units: %{{y:,}}<extra></extra>",
            ))
        sfig(fig4, h=400)
        fig4.update_layout(barmode="stack")
        fig4.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
        fig4.update_yaxes(title_text="<b>Total Units Sold</b>")
        st.plotly_chart(fig4, use_container_width=True)
        insight(
            "Stacked bars show the absolute sales volume per SR broken down by product. "
            "<strong>Taller bars = higher overall sales volume. "
            "The colour split reveals each SR's product portfolio composition.</strong> "
            "SRs dominated by a single colour are over-reliant on one product."
        )

        # -- Portfolio concentration -------------------------------------------
        section("SR Portfolio Concentration Analysis")
        conc = compute_product_concentration(_a_key, _ab)

        # Classify SRs
        def classify(hhi):
            if hhi >= 0.55:
                return "Highly Concentrated"
            elif hhi >= 0.35:
                return "Moderately Concentrated"
            else:
                return "Well Diversified"

        conc["Category"] = conc["HHI"].apply(classify)
        cat_colors = {
            "Highly Concentrated":      "#b91c1c",
            "Moderately Concentrated":  "#b45309",
            "Well Diversified":         "#15803d",
        }

        co1, co2 = st.columns(2)
        with co1:
            # HHI bar chart
            conc_sorted = conc.sort_values("HHI", ascending=False)
            bar_c = [cat_colors[c] for c in conc_sorted["Category"]]
            fig5 = go.Figure(go.Bar(
                x=conc_sorted["SRCode"],
                y=conc_sorted["HHI"],
                marker_color=bar_c,
                text=[f"<b>{v:.2f}</b>" for v in conc_sorted["HHI"]],
                textposition="outside",
                textfont=dict(color="#000000", size=11, family="Inter"),
                hovertemplate="<b>%{x}</b><br>HHI Score: %{y:.3f}<br>Dominant: " +
                               conc_sorted["DominantProduct"].iloc[0] + "<extra></extra>",
            ))
            fig5.add_hline(y=0.55, line_dash="dash", line_color="#b91c1c", line_width=1.5,
                           annotation_text="<b>Highly Concentrated</b>",
                           annotation_font=dict(color="#b91c1c", size=10, family="Inter"),
                           annotation_position="right")
            fig5.add_hline(y=0.35, line_dash="dash", line_color="#b45309", line_width=1.5,
                           annotation_text="<b>Moderately Concentrated</b>",
                           annotation_font=dict(color="#b45309", size=10, family="Inter"),
                           annotation_position="right")
            sfig(fig5, h=380, leg=False)
            fig5.update_layout(showlegend=False, yaxis_range=[0, 1.05])
            fig5.update_xaxes(title_text="<b>SR Code</b>", showgrid=False)
            fig5.update_yaxes(title_text="<b>Portfolio Concentration (HHI Score)</b>")
            st.plotly_chart(fig5, use_container_width=True)

        with co2:
            # Category summary table
            section("SR Portfolio Classification")
            disp_conc = conc_sorted[["SRCode", "DominantProduct", "DominantShare", "HHI", "Category"]].copy()
            disp_conc["DominantShare"] = (disp_conc["DominantShare"] * 100).round(1).astype(str) + "%"
            disp_conc["HHI"] = disp_conc["HHI"].round(3)
            st.dataframe(
                disp_conc.rename(columns={
                    "SRCode": "SR Code", "DominantProduct": "Top Product",
                    "DominantShare": "Top Product Share", "HHI": "HHI Score",
                    "Category": "Classification",
                }),
                use_container_width=True, hide_index=True,
            )
            # Category count cards
            for cat, color in cat_colors.items():
                n = int((conc["Category"] == cat).sum())
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:10px;'
                    f'margin:6px 0;padding:8px 14px;border-radius:8px;'
                    f'background:#f8fafc;border-left:4px solid {color};">'
                    f'<span style="font-size:18px;font-weight:900;color:{color};">{n}</span>'
                    f'<span style="font-size:13px;font-weight:700;color:#000;">{cat} SR{"s" if n!=1 else ""}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        insight(
            "The Herfindahl-Hirschman Index (HHI) measures portfolio concentration. "
            "<strong>HHI near 1.0 = sales almost entirely from one product (high risk). "
            "HHI near 0.2 = sales spread evenly across all products (well diversified).</strong> "
            "Red bars are SRs who depend too heavily on a single product -- "
            "they are vulnerable if that product faces supply or demand issues."
        )

        # -- Monthly product trends --------------------------------------------
        section("Monthly Sales Trend by Product")
        monthly_prod = compute_product_monthly(_a_key, _ab)

        fig6 = go.Figure()
        for prod in avail_products:
            fig6.add_trace(go.Scatter(
                x=monthly_prod["Month"],
                y=monthly_prod[prod],
                name=f"<b>{prod}</b>",
                line=dict(color=PRODUCT_COLORS.get(prod, "#64748b"), width=2.5),
                mode="lines+markers",
                marker=dict(size=7),
                hovertemplate=f"<b>{prod}</b><br>Month: %{{x}}<br>Units: %{{y:,}}<extra></extra>",
            ))
        sfig(fig6, h=380)
        fig6.update_xaxes(title_text="<b>Month</b>", showgrid=False)
        fig6.update_yaxes(title_text="<b>Units Sold</b>")
        st.plotly_chart(fig6, use_container_width=True)
        insight(
            "Monthly trend lines show whether each product is growing, declining, or staying flat over time. "
            "<strong>A widening gap between Parachute/Saffola and CocoSoul/Livon signals "
            "increasing portfolio concentration at the team level</strong>, which is a risk "
            "if primary products face market pressure. Rising CocoSoul or Livon lines "
            "would indicate successful portfolio expansion."
        )

        # -- Product coverage per SR (radar) ----------------------------------
        section("SR Product Coverage Radar")
        by_sr_norm = by_sr.copy()
        for prod in avail_products:
            mx = by_sr_norm[prod].max()
            by_sr_norm[prod] = (by_sr_norm[prod] / mx * 100).round(1) if mx > 0 else 0

        clrs = px.colors.qualitative.Bold
        fig7 = go.Figure()
        for i, row in by_sr_norm.iterrows():
            vals = [row[p] for p in avail_products]
            fig7.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=avail_products + [avail_products[0]],
                fill="toself",
                name=f"<b>{row['SRCode']}</b>",
                line_color=clrs[i % len(clrs)],
                opacity=0.65,
            ))
        fig7.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                 tickfont=dict(color="#000000", family="Inter", size=10)),
                angularaxis=dict(tickfont=dict(color="#000000", family="Inter", size=12)),
            ),
            height=460, paper_bgcolor="white", font=FONT,
            legend=dict(orientation="h", y=-0.12,
                         font=dict(color="#000000", family="Inter", size=11)),
            margin=dict(t=30, b=80, l=60, r=60),
        )
        st.plotly_chart(fig7, use_container_width=True)
        insight(
            "Each polygon shows one SR's product coverage normalised to 100% (best performer for each product). "
            "<strong>A large, symmetrical polygon means the SR sells all products at scale. "
            "A small or lopsided polygon reveals which specific products that SR neglects.</strong> "
            "Use this to identify targeted coaching opportunities per SR."
        )

        # -- Opportunity gap table ---------------------------------------------
        section("Untapped Sales Opportunity by SR and Product")
        team_avg = by_sr[avail_products].mean().round(0)
        gap_df   = by_sr.copy()
        for prod in avail_products:
            gap_df[f"{prod}_Gap"] = (team_avg[prod] - gap_df[prod]).clip(0).round(0).astype(int)

        gap_display = gap_df[["SRCode"] + [f"{p}_Gap" for p in avail_products]].copy()
        gap_display.columns = ["SR Code"] + [f"{p} Gap" for p in avail_products]
        gap_display["Total Opportunity"] = gap_display[[f"{p} Gap" for p in avail_products]].sum(axis=1)
        gap_display = gap_display.sort_values("Total Opportunity", ascending=False)
        st.dataframe(gap_display, use_container_width=True, hide_index=True)
        insight(
            "This table shows how many units below the team average each SR is for each product. "
            "<strong>Higher numbers = larger untapped opportunity.</strong> "
            "SRs with large gaps in CocoSoul and Livon are the primary targets for portfolio expansion coaching. "
            "Total Opportunity ranks which SRs have the most room for overall sales growth."
        )


# ===========================================================================
# PAGE: SR VS PRODUCT PERFORMANCE
# ===========================================================================
elif page == "SR vs Product Performance":
    st.markdown('<div class="pg-title">SR vs Product Performance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-sub">Deep-dive into how every sales representative performs across each '
        "product -- covering contribution, consistency, visit coverage, growth trends, "
        "and selling patterns. Use the SR selector below to inspect any individual in detail.</div>",
        unsafe_allow_html=True,
    )

    avail_products = [p for p in PRODUCTS if p in a.columns]

    if not avail_products:
        st.warning(
            "No product sales columns found. Please upload the enriched Actual Visits dataset "
            "that includes columns: " + ", ".join(PRODUCTS)
        )
    else:
        detail_df  = compute_sr_product_detail(_a_key, _ab)
        by_sr      = compute_product_by_sr(_a_key, _ab)
        conc       = compute_product_concentration(_a_key, _ab)
        monthly_sr = compute_sr_monthly_product(_a_key, _ab)

        all_srs = sorted(detail_df["SRCode"].unique())

        # ------------------------------------------------------------------ #
        # SECTION 1 -- TEAM-LEVEL SR x PRODUCT COMPARISON                   #
        # ------------------------------------------------------------------ #
        section("Team Overview -- SR Performance Across All Products")

        # Grouped bar: total qty per product per SR side-by-side
        fig_grp = go.Figure()
        for prod in avail_products:
            fig_grp.add_trace(go.Bar(
                name=f"<b>{prod}</b>",
                x=by_sr["SRCode"],
                y=by_sr[prod],
                marker_color=PRODUCT_COLORS.get(prod, "#64748b"),
                hovertemplate=(
                    f"<b>{prod}</b><br>SR: %{{x}}<br>Units: %{{y:,}}<extra></extra>"
                ),
            ))
        sfig(fig_grp, h=400)
        fig_grp.update_layout(barmode="group")
        fig_grp.update_xaxes(title_text="<b>Sales Representative</b>", showgrid=False)
        fig_grp.update_yaxes(title_text="<b>Total Units Sold</b>")
        st.plotly_chart(fig_grp, use_container_width=True)
        insight(
            "Grouped bars place every product side-by-side for each SR, making it immediately "
            "visible where individual SRs outperform or underperform the team. "
            "<strong>Tall bars across all products = well-rounded SR. "
            "One dominant bar = single-product dependency.</strong>"
        )

        # Coverage % heatmap (what % of visits resulted in a sale for each product)
        section("Visit Coverage -- What Percentage of an SR's Visits Include Each Product")
        cov_pivot = detail_df.pivot(index="SRCode", columns="Product", values="CoveragePct")
        cov_pivot = cov_pivot.reindex(columns=avail_products)

        fig_cov = px.imshow(
            cov_pivot,
            color_continuous_scale="RdYlGn",
            zmin=0, zmax=100,
            aspect="auto",
            labels=dict(x="<b>Product</b>", y="<b>SR Code</b>", color="<b>Coverage %</b>"),
            text_auto=".1f",
        )
        fig_cov.update_xaxes(title_text="<b>Product</b>",
                              title_font=dict(color="#000", family="Inter", size=13))
        fig_cov.update_yaxes(title_text="<b>SR Code</b>",
                              title_font=dict(color="#000", family="Inter", size=13))
        fig_cov.update_coloraxes(colorbar=dict(
            tickfont=dict(color="#000", family="Inter", size=11),
            title=dict(text="<b>% Visits</b>", font=dict(color="#000", family="Inter")),
        ))
        fig_cov.update_traces(textfont=dict(color="#000000", size=10, family="Inter"))
        fig_cov.update_layout(height=420, paper_bgcolor="white", font=FONT,
                               margin=dict(t=20, b=60, l=60, r=20))
        st.plotly_chart(fig_cov, use_container_width=True)
        insight(
            "Each cell shows the percentage of that SR's visits where the product was sold. "
            "<strong>Green = high coverage (product sold on most visits), "
            "red = low coverage (product rarely sold).</strong> "
            "White or red cells for CocoSoul and Livon confirm low penetration. "
            "Cells below 10% are immediate coaching targets."
        )

        # Avg qty per visit -- bubble chart
        section("Average Units Sold per Visit -- SR vs Product")
        avg_pivot = detail_df.pivot(index="SRCode", columns="Product", values="AvgQtyPerVisit")
        avg_melt  = avg_pivot.reset_index().melt(id_vars="SRCode",
                                                   value_vars=avail_products,
                                                   var_name="Product",
                                                   value_name="AvgQty")
        avg_melt["AvgQty"] = avg_melt["AvgQty"].fillna(0)

        fig_bub = px.scatter(
            avg_melt,
            x="SRCode", y="Product",
            size="AvgQty",
            color="AvgQty",
            color_continuous_scale="Blues",
            size_max=45,
            labels={
                "SRCode":  "<b>SR Code</b>",
                "Product": "<b>Product</b>",
                "AvgQty":  "<b>Avg Units / Visit</b>",
            },
            hover_data={"AvgQty": ":.2f"},
        )
        fig_bub.update_coloraxes(colorbar=dict(
            tickfont=dict(color="#000", family="Inter", size=11),
            title=dict(text="<b>Avg Units</b>", font=dict(color="#000", family="Inter")),
        ))
        fig_bub.update_layout(height=380, paper_bgcolor="white", font=FONT,
                               margin=dict(t=20, b=60, l=120, r=20))
        fig_bub.update_xaxes(**{**AXIS, "showgrid": False})
        fig_bub.update_yaxes(**{**AXIS, "showgrid": True, "gridcolor": "#f1f5f9"})
        st.plotly_chart(fig_bub, use_container_width=True)
        insight(
            "Bubble size and colour both encode average units sold per visit for that SR-product pair. "
            "<strong>Larger, darker bubbles = higher productivity per visit.</strong> "
            "Small bubbles don't necessarily mean low total sales -- the SR may visit many stores. "
            "Focus on product rows where most SRs have tiny bubbles to find team-wide underperformance."
        )

        # ------------------------------------------------------------------ #
        # SECTION 2 -- INDIVIDUAL SR DEEP DIVE                              #
        # ------------------------------------------------------------------ #
        st.markdown("<br>", unsafe_allow_html=True)
        section("Individual SR Deep Dive -- Select an SR to Inspect")

        col_sel, col_info = st.columns([1, 3])
        with col_sel:
            selected_sr = st.selectbox(
                "Choose Sales Representative",
                all_srs,
                key="sr_prod_selector",
                help="Select any SR to see their full product-level breakdown.",
            )

        sr_detail  = detail_df[detail_df["SRCode"] == selected_sr].set_index("Product")
        sr_conc    = conc[conc["SRCode"] == selected_sr].iloc[0] if len(conc[conc["SRCode"] == selected_sr]) else None
        sr_monthly = monthly_sr[monthly_sr["SRCode"] == selected_sr]
        sr_raw     = a[a["SRCode"] == selected_sr]

        with col_info:
            if sr_conc is not None:
                hhi_val = float(sr_conc["HHI"])
                hhi_cat = "Highly Concentrated" if hhi_val >= 0.55 else "Moderately Concentrated" if hhi_val >= 0.35 else "Well Diversified"
                hhi_col = "#b91c1c" if hhi_val >= 0.55 else "#b45309" if hhi_val >= 0.35 else "#15803d"
                dom_prod = sr_conc["DominantProduct"]
                dom_share = round(float(sr_conc["DominantShare"]) * 100, 1)
                total_qty = int(sr_conc["TotalQty"])
                st.markdown(
                    f'<div style="display:flex;gap:12px;flex-wrap:wrap;padding:8px 0;">'
                    f'<div style="background:#fff;border-radius:10px;padding:12px 18px;'
                    f'border-left:4px solid #1d4ed8;min-width:130px;">'
                    f'<div style="font-size:10px;font-weight:800;color:#64748b;text-transform:uppercase;'
                    f'letter-spacing:0.08em;">Total Units</div>'
                    f'<div style="font-size:22px;font-weight:900;color:#000;">{total_qty:,}</div></div>'
                    f'<div style="background:#fff;border-radius:10px;padding:12px 18px;'
                    f'border-left:4px solid {PRODUCT_COLORS.get(dom_prod,"#64748b")};min-width:130px;">'
                    f'<div style="font-size:10px;font-weight:800;color:#64748b;text-transform:uppercase;'
                    f'letter-spacing:0.08em;">Top Product</div>'
                    f'<div style="font-size:22px;font-weight:900;color:#000;">{dom_prod}</div>'
                    f'<div style="font-size:12px;font-weight:700;color:#475569;">{dom_share}% of sales</div></div>'
                    f'<div style="background:#fff;border-radius:10px;padding:12px 18px;'
                    f'border-left:4px solid {hhi_col};min-width:160px;">'
                    f'<div style="font-size:10px;font-weight:800;color:#64748b;text-transform:uppercase;'
                    f'letter-spacing:0.08em;">Portfolio Type</div>'
                    f'<div style="font-size:16px;font-weight:900;color:{hhi_col};">{hhi_cat}</div>'
                    f'<div style="font-size:12px;font-weight:700;color:#475569;">HHI: {hhi_val:.3f}</div></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # SR product breakdown: bar + radar side-by-side
        c1, c2 = st.columns(2)
        with c1:
            section(f"{selected_sr} -- Sales Volume per Product")
            sr_qty = sr_detail["TotalQty"].reindex(avail_products).fillna(0)
            bar_c  = [PRODUCT_COLORS.get(p, "#64748b") for p in avail_products]
            fig_sr_bar = go.Figure(go.Bar(
                x=avail_products,
                y=sr_qty.values,
                marker_color=bar_c,
                text=[f"<b>{int(v):,}</b>" for v in sr_qty.values],
                textposition="outside",
                textfont=dict(color="#000000", size=12, family="Inter"),
                hovertemplate="<b>%{x}</b><br>Units: %{y:,}<extra></extra>",
            ))
            sfig(fig_sr_bar, h=340, leg=False)
            fig_sr_bar.update_layout(showlegend=False)
            fig_sr_bar.update_xaxes(title_text="<b>Product</b>", showgrid=False)
            fig_sr_bar.update_yaxes(title_text="<b>Units Sold</b>")
            st.plotly_chart(fig_sr_bar, use_container_width=True)

        with c2:
            section(f"{selected_sr} -- Portfolio Shape (vs Team Average)")
            team_tot = by_sr[avail_products].mean()
            sr_tot   = by_sr[by_sr["SRCode"] == selected_sr][avail_products].values.flatten()
            # Normalise both to 0-100 against team max
            team_max = by_sr[avail_products].max()
            sr_norm   = (sr_tot   / team_max.replace(0, np.nan) * 100).fillna(0).tolist()
            team_norm = (team_tot / team_max.replace(0, np.nan) * 100).fillna(0).tolist()

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=team_norm + [team_norm[0]],
                theta=avail_products + [avail_products[0]],
                fill="toself", name="<b>Team Avg</b>",
                line=dict(color="#94a3b8", width=2, dash="dash"),
                fillcolor="rgba(148,163,184,0.12)",
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=sr_norm + [sr_norm[0]],
                theta=avail_products + [avail_products[0]],
                fill="toself", name=f"<b>{selected_sr}</b>",
                line=dict(color="#1d4ed8", width=3),
                fillcolor="rgba(29,78,216,0.15)",
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                     tickfont=dict(color="#000", family="Inter", size=10)),
                    angularaxis=dict(tickfont=dict(color="#000", family="Inter", size=12)),
                ),
                height=340, paper_bgcolor="white", font=FONT,
                legend=dict(orientation="h", y=-0.12,
                             font=dict(color="#000", family="Inter", size=11)),
                margin=dict(t=30, b=60, l=40, r=40),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        insight(
            "The bar chart shows absolute units sold per product for the selected SR. "
            "The radar chart overlays the SR's portfolio shape (blue) against the team average (grey dashed). "
            "<strong>When the blue polygon sits inside the grey, the SR is below team average for those products. "
            "When blue extends beyond grey, the SR outperforms the team for that product.</strong>"
        )

        # Detailed metrics table for selected SR
        section(f"{selected_sr} -- Product-Level Metrics Breakdown")
        sr_metrics_display = sr_detail[["TotalQty", "VisitsWithSale", "AvgQtyPerVisit",
                                         "CoveragePct", "Consistency", "MoMDelta"]].copy()
        sr_metrics_display = sr_metrics_display.reindex(avail_products).fillna(0)
        sr_metrics_display.index.name = "Product"
        sr_metrics_display.columns = [
            "Total Units", "Visits With Sale", "Avg Units/Visit",
            "Visit Coverage (%)", "Daily Consistency (Std)", "Growth (First vs Last Month)"
        ]
        # Colour-code the MoM delta
        sr_metrics_display["Growth (First vs Last Month)"] = sr_metrics_display[
            "Growth (First vs Last Month)"
        ].apply(lambda x: f"+{int(x)}" if x > 0 else str(int(x)))
        st.dataframe(sr_metrics_display.reset_index(), use_container_width=True, hide_index=True)
        insight(
            "Visit Coverage = percentage of this SR's visits where that product was sold. "
            "Daily Consistency (Std) = how much daily sales volume varies -- "
            "<strong>lower = more consistent selling pattern, higher = erratic.</strong> "
            "Growth shows whether sales of each product grew or shrank from the first to last month. "
            "Negative growth in core products is an early warning sign."
        )

        # Monthly trend for selected SR -- all products on one chart
        section(f"{selected_sr} -- Monthly Sales Trend per Product")
        fig_trend = go.Figure()
        for prod in avail_products:
            y_vals = sr_monthly[prod].values if prod in sr_monthly.columns else []
            fig_trend.add_trace(go.Scatter(
                x=sr_monthly["Month"],
                y=y_vals,
                name=f"<b>{prod}</b>",
                line=dict(color=PRODUCT_COLORS.get(prod, "#64748b"), width=2.5),
                mode="lines+markers",
                marker=dict(size=7),
                hovertemplate=f"<b>{prod}</b><br>Month: %{{x}}<br>Units: %{{y:,}}<extra></extra>",
            ))
        sfig(fig_trend, h=360)
        fig_trend.update_xaxes(title_text="<b>Month</b>", showgrid=False)
        fig_trend.update_yaxes(title_text="<b>Units Sold</b>")
        st.plotly_chart(fig_trend, use_container_width=True)
        insight(
            "Monthly trend lines for the selected SR show whether each product is growing or declining. "
            "<strong>A rising Parachute or Saffola line with flat CocoSoul/Livon lines "
            "confirms single-product concentration deepening over time.</strong> "
            "Look for any product lines that cross -- these indicate portfolio shifts worth investigating."
        )

        # Daily sales distribution per product -- box plots
        section(f"{selected_sr} -- Daily Sales Distribution per Product")
        daily_prod_data = []
        for prod in avail_products:
            daily_vals = sr_raw.groupby("Date")[prod].sum().reset_index()
            daily_vals["Product"] = prod
            daily_prod_data.append(daily_vals)
        daily_prod = pd.concat(daily_prod_data, ignore_index=True)

        fig_box = px.box(
            daily_prod, x="Product", y=prod,
            color="Product",
            color_discrete_map=PRODUCT_COLORS,
            labels={"Product": "<b>Product</b>", prod: "<b>Daily Units Sold</b>"},
            points="outliers",
        )
        # Rebuild properly using the melted frame
        fig_box2 = go.Figure()
        for prod in avail_products:
            vals = sr_raw.groupby("Date")[prod].sum().values
            fig_box2.add_trace(go.Box(
                y=vals,
                name=f"<b>{prod}</b>",
                marker_color=PRODUCT_COLORS.get(prod, "#64748b"),
                boxpoints="outliers",
                marker=dict(size=4),
                line=dict(width=2),
            ))
        sfig(fig_box2, h=360, leg=False)
        fig_box2.update_layout(showlegend=False)
        fig_box2.update_xaxes(title_text="<b>Product</b>", showgrid=False)
        fig_box2.update_yaxes(title_text="<b>Daily Units Sold</b>")
        st.plotly_chart(fig_box2, use_container_width=True)
        insight(
            "Box plots show how daily sales volume is distributed for each product. "
            "<strong>A tall box = high variability (inconsistent selling). "
            "A short box near zero = consistently low sales for that product.</strong> "
            "Outlier dots above the box are exceptional days -- check what drove them."
        )

        # ------------------------------------------------------------------ #
        # SECTION 3 -- TEAM COMPARISON TABLES                                #
        # ------------------------------------------------------------------ #
        st.markdown("<br>", unsafe_allow_html=True)
        section("Full Team -- SR vs Product Comparison Table")

        # Build a clean summary table: SRCode + one column per product (total qty) + total + rank
        summary = by_sr.copy()
        summary["Total Units"] = summary[avail_products].sum(axis=1).astype(int)
        summary["Rank"] = summary["Total Units"].rank(ascending=False).astype(int)
        for prod in avail_products:
            summary[prod] = summary[prod].astype(int)
        summary = summary.sort_values("Total Units", ascending=False)
        st.dataframe(
            summary[["SRCode"] + avail_products + ["Total Units", "Rank"]].rename(
                columns={"SRCode": "SR Code"}
            ),
            use_container_width=True, hide_index=True,
        )

        # Consistency ranking table
        section("Product Selling Consistency -- Who Sells Each Product Most Reliably")
        consist_pivot = detail_df.pivot(index="SRCode", columns="Product", values="CoveragePct")
        consist_pivot = consist_pivot.reindex(columns=avail_products).fillna(0).round(1)
        consist_pivot["Avg Coverage"] = consist_pivot[avail_products].mean(axis=1).round(1)
        consist_pivot = consist_pivot.sort_values("Avg Coverage", ascending=False).reset_index()
        # Format as percentages
        for col in avail_products + ["Avg Coverage"]:
            consist_pivot[col] = consist_pivot[col].apply(lambda x: f"{x:.1f}%")
        st.dataframe(
            consist_pivot.rename(columns={"SRCode": "SR Code"}),
            use_container_width=True, hide_index=True,
        )
        insight(
            "Visit Coverage (%) = the percentage of an SR's total visits where they sold at least one unit "
            "of that product. <strong>Average Coverage summarises overall product portfolio breadth. "
            "SRs with high average coverage sell across all products consistently -- "
            "they are your most versatile team members.</strong> "
            "SRs at the bottom with low coverage across secondary products are specialised but fragile."
        )


# ---------------------------------------------------------------------------
# BOTTOM NAVIGATION  --  rendered at the end of every page
# ---------------------------------------------------------------------------
if data_ready:
    nav_buttons()
