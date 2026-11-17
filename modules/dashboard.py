
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


st.set_page_config(
    page_title="Signal Stack AI",
    page_icon="📊",
    layout="wide"
)


def show_analysis(title, function, signals):
    """Safely display an intelligence analysis section."""

    st.subheader(title)

    if not signals:
        st.info("Add signals to generate this analysis.")
        return

    try:
        result = function(signals)

        if result is None:
            st.info("No analysis available yet.")

        elif isinstance(result, pd.DataFrame):
            if not result.empty:
                st.dataframe(result, use_container_width=True)
            else:
                st.info("No data available.")

        elif isinstance(result, dict):
            for key, value in result.items():
                st.write(f"**{str(key).replace('_', ' ').title()}**")
                if isinstance(value, (dict, list)):
                    st.write(value)
                else:
                    st.write(value)

        elif isinstance(result, list):
            if result:
                for item in result:
                    st.write(item)
            else:
                st.info("No results available.")

        else:
            st.write(result)

    except Exception as error:
        st.warning(f"Analysis could not be generated: {error}")


def render_dashboard():

    st.title("📊 Signal Stack AI")

    st.caption(
        "Intelligent Business Signal Monitoring and Analysis"
    )

    # ==========================================
    # ADD SIGNAL
    # ==========================================

    st.sidebar.header("➕ Add Intelligence Signal")

    with st.sidebar.form("add_signal_form"):

        title = st.text_input(
            "Signal Title",
            placeholder="Example: Competitor launches a new AI product"
        )

        content = st.text_area(
            "Signal Description",
            placeholder="Describe the business intelligence signal..."
        )

        source = st.text_input(
            "Source",
            placeholder="Example: News, Website, Report"
        )

        submitted = st.form_submit_button(
            "Process and Save Signal",
            use_container_width=True
        )

        if submitted:

            if not title.strip() or not content.strip():
                st.error("Please enter both a title and description.")

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
                            "This signal already exists in the database."
                        )

                except Exception as error:
                    st.sidebar.error(
                        f"Could not process signal: {error}"
                    )

    # ==========================================
    # RETRIEVE SIGNALS
    # ==========================================

    try:
        raw_signals = get_prioritized_signals()
        signals = [dict(signal) for signal in raw_signals]

    except Exception as error:
        st.error(f"Unable to retrieve signals: {error}")
        signals = []

    st.divider()

    # ==========================================
    # OVERVIEW
    # ==========================================

    st.header("📈 Intelligence Overview")

    total_signals = len(signals)

    if signals:
        df = pd.DataFrame(signals)

        if "category" not in df.columns:
            df["category"] = "Unclassified"

        if "priority_score" not in df.columns:
            df["priority_score"] = 0

        if "relevance_score" not in df.columns:
            df["relevance_score"] = 0

        df["priority_score"] = pd.to_numeric(
            df["priority_score"], errors="coerce"
        ).fillna(0)

        df["relevance_score"] = pd.to_numeric(
            df["relevance_score"], errors="coerce"
        ).fillna(0)

        high_priority = len(
            df[df["priority_score"] >= 70]
        )

        average_relevance = df["relevance_score"].mean()

        categories_count = df["category"].nunique()

    else:
        df = pd.DataFrame(
            columns=[
                "title",
                "content",
                "source",
                "category",
                "priority_score",
                "relevance_score"
            ]
        )

        high_priority = 0
        average_relevance = 0
        categories_count = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Signals", total_signals)

    col2.metric("High Priority Signals", high_priority)

    col3.metric(
        "Average Relevance",
        f"{average_relevance:.1f}"
    )

    col4.metric("Intelligence Categories", categories_count)

    st.divider()

    # ==========================================
    # FILTERS
    # ==========================================

    st.header("🔎 Signal Explorer")

    if signals:

        category_options = ["All"] + sorted(
            df["category"].dropna().astype(str).unique().tolist()
        )

        selected_category = st.selectbox(
            "Filter by Category",
            category_options
        )

        search_text = st.text_input(
            "Search Signals",
            placeholder="Search title, content or source..."
        )

        filtered = df.copy()

        if selected_category != "All":
            filtered = filtered[
                filtered["category"] == selected_category
            ]

        if search_text.strip():

            search_mask = (
                filtered["title"].fillna("").astype(str).str.contains(
                    search_text, case=False, na=False
                )
                |
                filtered["content"].fillna("").astype(str).str.contains(
                    search_text, case=False, na=False
                )
                |
                filtered["source"].fillna("").astype(str).str.contains(
                    search_text, case=False, na=False
                )
            )

            filtered = filtered[search_mask]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No signals available yet. Use the Add Intelligence Signal "
            "form in the sidebar to begin."
        )

    st.divider()

    # ==========================================
    # PRIORITY INTELLIGENCE
    # ==========================================

    st.header("🚨 Priority Intelligence")

    if signals:

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
        st.info("Priority intelligence will appear after adding signals.")

    st.divider()

    # ==========================================
    # SIGNAL DISTRIBUTION
    # ==========================================

    st.header("📊 Signal Distribution")

    if signals:

        col1, col2 = st.columns(2)

        with col1:
            category_data = (
                df["category"]
                .fillna("Unclassified")
                .value_counts()
                .reset_index()
            )

            category_data.columns = ["Category", "Count"]

            fig = px.pie(
                category_data,
                names="Category",
                values="Count",
                title="Signals by Category",
                hole=0.4
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                df.sort_values(
                    "priority_score",
                    ascending=False
                ).head(10),
                x="title",
                y="priority_score",
                title="Top 10 Signal Priority Scores"
            )

            fig.update_layout(xaxis_title="Signal")

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Charts will appear when signals are available.")

    st.divider()

    # ==========================================
    # TREND INTELLIGENCE
    # ==========================================

    show_analysis(
        "📈 Trend Intelligence",
        generate_trend_report,
        signals
    )

    st.divider()

    # ==========================================
    # COMPETITOR INTELLIGENCE
    # ==========================================

    show_analysis(
        "🏢 Competitor Intelligence",
        analyze_competitors,
        signals
    )

    st.divider()

    # ==========================================
    # CUSTOMER INTELLIGENCE
    # ==========================================

    show_analysis(
        "👥 Customer Intelligence",
        analyze_customers,
        signals
    )

    st.divider()

    # ==========================================
    # MARKET INTELLIGENCE
    # ==========================================

    show_analysis(
        "🌍 Market Intelligence",
        analyze_market,
        signals
    )

    st.divider()

    # ==========================================
    # INTERNAL INTELLIGENCE
    # ==========================================

    show_analysis(
        "🏭 Internal Intelligence",
        analyze_internal,
        signals
    )

    st.divider()

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    show_analysis(
        "🧠 Executive Intelligence Summary",
        generate_executive_summary,
        signals
    )

    st.divider()

    st.caption(
        "Signal Stack AI | Intelligent Business Signal Monitoring"
    )


render_dashboard()
