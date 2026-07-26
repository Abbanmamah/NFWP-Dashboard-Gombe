from utils.database import ensure_database
ensure_database()

ensure_database()

from utils.kobo_sync import sync_kobo
from utils.kobo_sync import load_last_sync
import streamlit as st

import pandas as pd
from io import BytesIO

from utils.data_loader import (
    load_membership_data,
    load_savings_data,
)

from utils.calculations import (
    calculate_total_wags,
    calculate_total_members,
    calculate_total_savings,
    calculate_total_loan_fund,
    calculate_total_loan_disbursed,
    calculate_total_loan_repaid,
    calculate_outstanding_loan,
    calculate_average_loan_utilisation,
)

from utils.lga_summary import get_lga_summary

from utils.charts import (
    chart_wags,
    chart_members,
    chart_savings,
    chart_loans,
)

from utils.monthly_trends import get_monthly_trends

from utils.wag_profile import get_wag_profile

from utils.data_quality import get_data_quality

from utils.top_wags import get_top_wags

from utils.report_export import create_management_report

import pandas as pd

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="NFWP-SU Gombe Dashboard",
    page_icon="📊",
    layout="wide",
)

# =====================================================
# NFWP THEME
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F7F9FA;
    }

    h1 {
        color: #006838;
        font-weight: bold;
    }

    h2 {
        color: #006838;
    }

    h3 {
        color: #006838;
    }

    hr {
        border: 1px solid #D9D9D9;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# PROFESSIONAL HEADER
# =====================================================

header_logo, header_text = st.columns([1, 7])

with header_logo:
    st.image("assets/logo.png", width=100)

with header_text:
    st.markdown(
        """
# NFWP-SU Gombe State Dashboard
### Nigeria for Women Programme – Scale Up
##### Management Information System
"""
    )

st.divider()

# ======================================
# KOBO SYNC
# ======================================

col_sync1, col_sync2 = st.columns([1, 5])

with col_sync1:

    if st.button("🔄 Sync Latest Kobo Data"):

        with st.spinner("Downloading latest Kobo submissions..."):

            result = sync_kobo()

        st.success(
            f"""
✅ Sync Completed

Membership Added: {result['membership_added']}

Savings Added: {result['savings_added']}
"""
        )

        st.rerun()

# ======================================
# LAST SYNC STATUS
# ======================================

sync_info = load_last_sync()

st.info(
    f"""
🔄 **Last Sync**

**Date & Time:** {sync_info.get('membership', 'Never')}

**Membership Added:** {sync_info.get('membership_added', 0)}

**Savings Added:** {sync_info.get('savings_added', 0)}
"""
)
        
# =====================================================
# LOAD DATA
# =====================================================

with st.spinner("Loading dashboard data..."):
    membership = load_membership_data()
    savings = load_savings_data()

# ======================================
# LOCATION FILTERS
# ======================================

filter1, filter2, filter3 = st.columns(3)

# -----------------------------
# LGA
# -----------------------------

lga_options = sorted(
    list(
        set(
            record.get("location_details/lga", "Unknown")
            for record in membership
        )
    )
)

selected_lga = filter1.selectbox(
    "📍 LGA",
    ["All LGAs"] + lga_options
)

# -----------------------------
# WARD
# -----------------------------

ward_records = membership

if selected_lga != "All LGAs":
    ward_records = [
        r for r in membership
        if r.get("location_details/lga") == selected_lga
    ]

ward_options = sorted(
    list(
        set(
            r.get("location_details/ward", "Unknown")
            for r in ward_records
        )
    )
)

selected_ward = filter2.selectbox(
    "🏘 Ward",
    ["All Wards"] + ward_options
)

# -----------------------------
# COMMUNITY
# -----------------------------

community_records = ward_records

if selected_ward != "All Wards":
    community_records = [
        r for r in ward_records
        if r.get("location_details/ward") == selected_ward
    ]

community_options = sorted(
    list(
        set(
            r.get("location_details/community", "Unknown")
            for r in community_records
        )
    )
)

selected_community = filter3.selectbox(
    "🏡 Community",
    ["All Communities"] + community_options
)

# -----------------------------
# APPLY FILTERS
# -----------------------------

def matches(record):

    if (
        selected_lga != "All LGAs"
        and record.get("location_details/lga") != selected_lga
    ):
        return False

    if (
        selected_ward != "All Wards"
        and record.get("location_details/ward") != selected_ward
    ):
        return False

    if (
        selected_community != "All Communities"
        and record.get("location_details/community") != selected_community
    ):
        return False

    return True

membership = [
    r for r in membership
    if matches(r)
]

savings = [
    r for r in savings
    if matches(r)
]    

# ======================================
# WEEK FILTER
# ======================================

week_options = sorted(
    list(
        set(
            record.get("location_details/savings_week", "Unknown")
            for record in savings
        )
    )
)

selected_week = st.selectbox(
    "📅 Select Savings Week",
    ["All Weeks"] + week_options
)

if selected_week != "All Weeks":

    savings = [
        record
        for record in savings
        if record.get("location_details/savings_week") == selected_week
    ]

st.divider()

st.header("📈 Executive Dashboard")
st.caption("Key Performance Indicators for NFWP-SU Gombe State")

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_wags = calculate_total_wags(membership)
total_members = calculate_total_members(membership)
total_savings = calculate_total_savings(savings)
total_loan_fund = calculate_total_loan_fund(savings)
total_loan_disbursed = calculate_total_loan_disbursed(savings)
total_loan_repaid = calculate_total_loan_repaid(savings)
outstanding_loan = calculate_outstanding_loan(savings)
loan_utilisation = calculate_average_loan_utilisation(savings)

st.divider()

def kpi_card(title, value, color="#006838"):
    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:20px;
            border-radius:15px;
            color:white;
            text-align:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.15);
            margin-bottom:15px;
        ">
            <div style="font-size:18px;font-weight:bold;">
                {title}
            </div>

            <div style="font-size:32px;font-weight:bold;margin-top:12px;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================
# KPI ROW 1
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Total WAGs",
        f"{total_wags:,}"
    )

with col2:
    st.metric(
        "👩 Total Members",
        f"{total_members:,}"
    )

with col3:
    st.metric(
        "💰 Total Savings Fund",
        f"₦{total_savings:,.2f}"
    )

# =====================================================
# KPI ROW 2
# =====================================================

col4, col5, col6 = st.columns(3)

col4.metric(
    "🏦 Total Loan Fund",
    f"₦{total_loan_fund:,.2f}"
)

col5.metric(
    "💸 Total Loan Disbursed",
    f"₦{total_loan_disbursed:,.2f}"
)

col6.metric(
    "💵 Total Loan Repaid",
    f"₦{total_loan_repaid:,.2f}"
)

# =====================================================
# KPI ROW 3
# =====================================================

col7, col8 = st.columns(2)

col7.metric(
    "📉 Outstanding Loan",
    f"₦{outstanding_loan:,.2f}"
)

col8.metric(
    "📊 Average Loan Utilisation",
    f"{loan_utilisation:.1f}%"
)

st.divider()

# =====================================================
# LGA SUMMARY
# =====================================================

# ======================================
# EXPORT LGA SUMMARY TO EXCEL
# ======================================

def export_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="LGA Summary"
        )

    return output.getvalue()

st.divider()
st.header("📍 LGA Performance")
st.caption("Summary of WAG activities across the 3 LGAs")

summary = get_lga_summary(membership, savings)

rows = []

for lga, values in summary.items():

    rows.append({

        "LGA": lga,

        "WAGs": values["WAGs"],

        "Members": values["Members"],

        "Savings": f"₦{values['Savings']:,.2f}",

        "Loan Fund": f"₦{values['Loan Fund']:,.2f}",

        "Loan Disbursed": f"₦{values['Loan Disbursed']:,.2f}",

        "Loan Repaid": f"₦{values['Loan Repaid']:,.2f}",

        "Average Loan Utilisation": f"{values['Average Loan Utilisation']:.1f}%",

    })

df = pd.DataFrame(rows)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

excel_file = export_to_excel(df)

st.download_button(
    label="📥 Download LGA Summary (Excel)",
    data=excel_file,
    file_name="NFWP_Gombe_LGA_Summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# =====================================================
# CHARTS
# =====================================================

st.divider()

with st.expander("📊 Dashboard Charts", expanded=True):

    st.markdown("### LGA Performance Charts")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.plotly_chart(
            chart_wags(summary),
            use_container_width=True,
        )

    with chart2:
        st.plotly_chart(
            chart_members(summary),
            use_container_width=True,
        )

    chart3, chart4 = st.columns(2)

    with chart3:
        st.plotly_chart(
            chart_savings(summary),
            use_container_width=True,
        )

    with chart4:
        st.plotly_chart(
            chart_loans(summary),
            use_container_width=True,
        )
        
# ==================================================
# MONTHLY TREND CHARTS
# ==================================================

st.divider()

monthly = get_monthly_trends(savings)

trend_df = (
    pd.DataFrame(monthly)
    .T
    .reset_index()
    .rename(columns={"index": "Month"})
)

with st.expander("📈 Monthly Trends", expanded=False):

    st.markdown("### Monthly Financial Trends")

    trend1, trend2 = st.columns(2)

    with trend1:
        st.markdown("#### 💰 Savings by Month")
        st.line_chart(
            trend_df.set_index("Month")["Savings"],
            use_container_width=True,
        )

    with trend2:
        st.markdown("#### 💸 Loan Disbursed by Month")
        st.line_chart(
            trend_df.set_index("Month")["Loan Disbursed"],
            use_container_width=True,
        )

    st.markdown("#### 💵 Loan Repaid by Month")
    st.line_chart(
        trend_df.set_index("Month")["Loan Repaid"],
        use_container_width=True,
    )

# ======================================
# WAG SEARCH
# ======================================

st.divider()
st.subheader("🔍 WAG Search")

search = st.text_input(
    "Search by WAG ID, WAG Name, LGA, Ward or Community"
)

if search:

    search = search.lower().strip()

    rows = []

    for saving in savings:

        wag_id = str(saving.get("location_details/wag_id", ""))
        wag_name = str(saving.get("location_details/wagname", ""))
        lga = str(saving.get("location_details/lga", ""))
        ward = str(saving.get("location_details/ward", ""))
        community = str(saving.get("location_details/community", ""))

        text = " ".join([
            wag_id,
            wag_name,
            lga,
            ward,
            community
        ]).lower()

        if search in text:

            # Find corresponding membership record
            members_count = 0
            wf_name = ""

            for member in membership:

                if member.get("location_details/wagid", "") == wag_id:

                    member_list = member.get("mem_det/member_details", [])

                    if isinstance(member_list, list):
                        members_count = len(member_list)

                    wf_name = member.get("wfname", "")
                    break

            rows.append({

                "WAG ID": wag_id,
                "WAG Name": wag_name,
                "LGA": lga,
                "Ward": ward,
                "Community": community,
                "Ward Facilitator": wf_name,
                "Members": members_count,
                "Savings": f"₦{float(saving.get('lf_section/total_savings',0)):,.2f}",
                "Loan Fund": f"₦{float(saving.get('lf_section/tlfc',0)):,.2f}",
                "Loan Disbursed": f"₦{float(saving.get('ld_dis_act/total_loans_given',0)):,.2f}",
                "Loan Repaid": f"₦{float(saving.get('repayments/total_repayments_made',0)):,.2f}",
                "Average Loan Utilisation": f"{float(saving.get('begin_group_L6KqAQmFs/lur',0)):.1f}%",

            })

    if rows:

        df_search = pd.DataFrame(rows)

        st.success(f"Found {len(df_search):,} matching WAG(s).")

        st.dataframe(
            df_search,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.warning("No matching WAG found.")

# =====================================================
# TOP & BOTTOM 10 WAGS
# =====================================================

st.divider()

st.subheader("🏆 WAG Performance Ranking")

col1, col2 = st.columns(2)

# -----------------------------
# TOP 10
# -----------------------------

with col1:

    st.markdown("### 🥇 Top 10 WAGs by Savings")

    top10 = get_top_wags(savings, top=True)

    if top10:

        top_df = pd.DataFrame(top10)

        top_df.insert(
            0,
            "Rank",
            range(1, len(top_df) + 1)
        )

        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True
        )

# -----------------------------
# BOTTOM 10
# -----------------------------

with col2:

    st.markdown("### 📉 Bottom 10 WAGs by Savings")

    bottom10 = get_top_wags(savings, top=False)

    if bottom10:

        bottom_df = pd.DataFrame(bottom10)

        bottom_df.insert(
            0,
            "Rank",
            range(1, len(bottom_df) + 1)
        )

        st.dataframe(
            bottom_df,
            use_container_width=True,
            hide_index=True
        )

# =====================================================
# DATA QUALITY DASHBOARD
# =====================================================

st.divider()

st.subheader("🚨 Data Quality Dashboard")

dq = get_data_quality(membership, savings)

# ==========================
# ROW 1
# ==========================

row1 = st.columns(2)

row1[0].metric(
    "📋 Membership Records",
    f"{dq['Membership Records']:,}"
)

row1[1].metric(
    "💾 Savings Records",
    f"{dq['Savings Records']:,}"
)

# ==========================
# ROW 2
# ==========================

row2 = st.columns(2)

row2[0].metric(
    "🔁 Duplicate Membership IDs",
    f"{dq['Duplicate Membership IDs']:,}"
)

row2[1].metric(
    "🔁 Duplicate Savings IDs",
    f"{dq['Duplicate Savings IDs']:,}"
)

# ==========================
# ROW 3
# ==========================

row3 = st.columns(4)

row3[0].metric(
    "📍 Missing GPS",
    f"{dq['Missing GPS']:,}"
)

row3[1].metric(
    "🏘 Missing Ward",
    f"{dq['Missing Ward']:,}"
)

row3[2].metric(
    "🏡 Missing Community",
    f"{dq['Missing Community']:,}"
)

row3[3].metric(
    "👥 Zero Members",
    f"{dq['Zero Members']:,}"
)

# ==========================
# SUMMARY STATUS
# ==========================

issues = (
    dq["Duplicate Membership IDs"]
    + dq["Duplicate Savings IDs"]
    + dq["Missing GPS"]
    + dq["Missing Ward"]
    + dq["Missing Community"]
    + dq["Zero Members"]
)

if issues == 0:
    st.success("✅ No data quality issues detected.")
else:
    st.warning(
        f"⚠ {issues:,} data quality issue(s) detected. Please review before reporting."
    )

report = create_management_report(
    summary_df=df,
    trend_df=trend_df,
    dq=dq,
    top_df=top_df,
    bottom_df=bottom_df,
    total_wags=total_wags,
    total_members=total_members,
    total_savings=total_savings,
    total_loan_fund=total_loan_fund,
    total_loan_disbursed=total_loan_disbursed,
    total_loan_repaid=total_loan_repaid,
    outstanding_loan=outstanding_loan,
    average_utilisation=loan_utilisation,
)

st.download_button(
    "📊 Download Management Report",
    data=report,
    file_name="NFWP_Gombe_Management_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.success("✅ Dashboard loaded successfully.")