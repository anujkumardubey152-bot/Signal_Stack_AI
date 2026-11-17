
"""
Signal Stack AI
Intelligent Business Signal Monitoring and Analysis Dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.pipeline import process_signal, get_prioritized_signals

from modules.trend_analyzer import generate_trend_report
from modules.competitor_analyzer import analyze_competitors
from modules.customer_analyzer import analyze_customers
from modules.market_analyzer import analyze_market
from modules.internal_analyzer import analyze_internal
from modules.executive_summary import generate_executive_summary


# ==========================================
# ANALYSIS DISPLAY
# ==========================================

def show_analysis(title, function, signals):

    st.subheader(title)

    if not signals:
        st.info("Add intelligence signals to generate this analysis.")
        return

    try:
        result = function(signals)

        if result is None:
            st.info("No analysis available yet.")

        elif isinstance(result, pd.DataFrame):

            if result.empty:
                st.info("No analysis data available.")
            else:
                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

        elif isinstance(result, dict):

            if not result:
                st.info("No analysis results available.")
            else:
                for key, value in result.items():

                    st.markdown(
                        f"**{str(key).replace('_', ' ').title()}**"
                    )

                    if isinstance(value, (dict, list)):
                        st.write(value)
                    else:
                        st.write(value)

        elif isinstance(result, list):

            if not result:
                st.info("No results available.")
            else:
                for item in result:
                    st.write(item)

        else:
            st.write(result)

    except Exception as error:

        st.warning(
            f"Unable to generate {title}: {error}"
        )


# ==========================================
# MAIN DASHBOARD
# ==========================================

def render_dashboard():

    # ======================================
    # HEADER
    # ======================================

    st.title("📊 Signal Stack AI")

    st.caption(
        "Intelligent Business Signal Monitoring and Analysis"
    )

    st.markdown(
        "Monitor business signals, discover opportunities, "
        "track competitors, and generate actionable intelligence."
    )

    # ======================================
    # ADD SIGNAL FORM
    # ======================================

    st.sidebar.title("⚙️ Signal Management")

    st.sidebar.subheader("➕ Add Intelligence Signal")

    with st.sidebar.form("add_signal_form"):

        title = st.text_input(
            "Signal Title",
            placeholder="Enter signal title"
        )

        content = st.text_area(
            "Signal Description",
            placeholder="Describe the intelligence signal..."
        )

        source = st.text_input(
            "Signal Source",
            placeholder="News, Website, Report, etc."
        )

        submitted = st.form_submit_button(
            "🚀 Process and Save Signal",
            use_container_width=True
        )

        if submitted:

            if not title.strip() or not content.strip():

                st.sidebar.error(
                    "Please enter both title and description."
                )

            else:

                signal = {
                    "title": title.strip(),
                    "content": content.strip(),
                    "source": source.strip()
                }

                try:

                    result = process_signal(signal)

                    if result.get("status") == "Saved":

                        st.sidebar.success(
                            "Signal successfully processed and saved!"
                        )

                        st.rerun()

                    else:

                        st.sidebar.warning(
                            "Duplicate signal detected. "
                            "This signal already exists."
                        )

                except Exception as error:

                    st.sidebar.error(
                        f"Signal processing failed: {error}"
                    )

    # ======================================
    # DATABASE RETRIEVAL
    # ======================================

    try:

        raw_signals = get_prioritized_signals()

        signals = [
            dict(signal)
            for signal in raw_signals
        ]

    except Exception as error:

        st.error(
            f"Database retrieval failed: {error}"
        )

        signals = []

    st.divider()

    # ======================================
    # DATA PREPARATION
    # ======================================

    df = pd.DataFrame(signals)

    required_columns = {
        "title": "",
        "content": "",
        "source": "",
        "category": "Unclassified",
        "priority_score": 0,
        "relevance_score": 0
    }

    for column, default in required_columns.items():

        if column not in df.columns:
            df[column] = default

    df["priority_score"] = pd.to_numeric(
        df["priority_score"],
        errors="coerce"
    ).fillna(0)

    df["relevance_score"] = pd.to_numeric(
        df["relevance_score"],
        errors="coerce"
    ).fillna(0)

    # ======================================
    # OVERVIEW METRICS
    # ======================================

    st.header("📈 Intelligence Overview")

    total_signals = len(df)

    high_priority = len(
        df[df["priority_score"] >= 70]
    )

    average_relevance = (
        df["relevance_score"].mean()
        if total_signals else 0
    )

    categories_count = (
        df["category"].nunique()
        if total_signals else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Signals",
        total_signals
    )

    col2.metric(
        "High Priority",
        high_priority
    )

    col3.metric(
        "Average Relevance",
        f"{average_relevance:.1f}"
    )

    col4.metric(
        "Categories",
        categories_count
    )

    st.divider()

    # ======================================
    # SIGNAL EXPLORER
    # ======================================

    st.header("🔎 Signal Explorer")

    if total_signals:

        category_options = ["All"] + sorted(
            df["category"]
            .fillna("Unclassified")
            .astype(str)
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Filter by Category",
            category_options
        )

        search_text = st.text_input(
            "Search Signals",
            placeholder="Search title, description or source..."
        )

        filtered = df.copy()

        if selected_category != "All":

            filtered = filtered[
                filtered["category"] == selected_category
            ]

        if search_text.strip():

            search_mask = (

                filtered["title"]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )

                |

                filtered["content"]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )

                |

                filtered["source"]
                .fillna("")
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )

            )

            filtered = filtered[search_mask]

        st.write(
            f"Showing {len(filtered)} of {total_signals} signals"
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No signals available yet. "
            "Use the Add Intelligence Signal form in the sidebar."
        )

    st.divider()

    # ======================================
    # PRIORITY INTELLIGENCE
    # ======================================

    st.header("🚨 Priority Intelligence")

    if total_signals:

        priority_df = df.sort_values(
            "priority_score",
            ascending=False
        ).head(10)

        st.dataframe(
            priority_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Priority intelligence will appear after adding signals."
        )

    st.divider()

    # ======================================
    # SIGNAL DISTRIBUTION
    # ======================================

    st.header("📊 Signal Distribution")

    if total_signals:

        col1, col2 = st.columns(2)

        with col1:

            category_data = (
                df["category"]
                .fillna("Unclassified")
                .value_counts()
                .reset_index()
            )

            category_data.columns = [
                "Category",
                "Count"
            ]

            fig = px.pie(
                category_data,
                names="Category",
                values="Count",
                title="Signals by Category",
                hole=0.4
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            chart_df = (
                df.sort_values(
                    "priority_score",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                chart_df,
                x="title",
                y="priority_score",
                title="Top 10 Priority Signals"
            )

            fig.update_layout(
                xaxis_title="Signal",
                yaxis_title="Priority Score"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info(
            "Charts will be generated when signals are available."
        )

    st.divider()

    # ======================================
    # TREND INTELLIGENCE
    # ======================================

    show_analysis(
        "📈 Trend Intelligence",
        generate_trend_report,
        signals
    )

    st.divider()

    # ======================================
    # COMPETITOR INTELLIGENCE
    # ======================================

    show_analysis(
        "🏢 Competitor Intelligence",
        analyze_competitors,
        signals
    )

    st.divider()

    # ======================================
    # CUSTOMER INTELLIGENCE
    # ======================================

    show_analysis(
        "👥 Customer Intelligence",
        analyze_customers,
        signals
    )

    st.divider()

    # ======================================
    # MARKET INTELLIGENCE
    # ======================================

    show_analysis(
        "🌍 Market Intelligence",
        analyze_market,
        signals
    )

    st.divider()

    # ======================================
    # INTERNAL INTELLIGENCE
    # ======================================

    show_analysis(
        "🏭 Internal Intelligence",
        analyze_internal,
        signals
    )

    st.divider()

    # ======================================
    # EXECUTIVE SUMMARY
    # ======================================

    show_analysis(
        "🧠 Executive Intelligence Summary",
        generate_executive_summary,
        signals
    )

    st.divider()

    # ======================================
    # FOOTER
    # ======================================

    st.caption(
        "Signal Stack AI | Intelligent Business Signal Monitoring"
    )
