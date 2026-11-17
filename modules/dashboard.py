
import streamlit as st
import pandas as pd
import plotly.express as px

from modules.pipeline import get_prioritized_signals
from modules.trend_analyzer import generate_trend_report
from modules.competitor_analyzer import analyze_competitors
from modules.customer_analyzer import analyze_customers
from modules.market_analyzer import analyze_market
from modules.internal_analyzer import analyze_internal
from modules.executive_summary import generate_executive_summary


def safe_dataframe(data):
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.DataFrame(data)
    return pd.DataFrame()


def render_dashboard():

    st.set_page_config(
        page_title="Signal Stack AI",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Signal Stack AI")
    st.caption("Intelligent Business Signal Monitoring and Analysis")

    # LOAD SIGNALS
    signals = get_prioritized_signals()

    if not signals:
        st.info("No signals available yet. Add signals to begin.")
        return

    df = pd.DataFrame(signals)

    defaults = {
        "title": "",
        "content": "",
        "category": "Internal",
        "priority": "Normal",
        "priority_score": 0,
        "relevance_score": 0,
        "source": "Unknown"
    }

    for column, default in defaults.items():
        if column not in df.columns:
            df[column] = default

    df["priority_score"] = pd.to_numeric(
        df["priority_score"], errors="coerce"
    ).fillna(0)

    df["relevance_score"] = pd.to_numeric(
        df["relevance_score"], errors="coerce"
    ).fillna(0)

    # OVERVIEW
    st.subheader("📌 Intelligence Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Signals", len(df))
    c2.metric(
        "High Priority",
        int(df["priority"].astype(str).str.lower().isin(
            ["high", "critical", "urgent"]
        ).sum())
    )
    c3.metric("Categories", df["category"].nunique())
    c4.metric("Sources", df["source"].nunique())

    st.divider()

    # FILTERS
    st.subheader("🔎 Filter Signals")

    f1, f2, f3 = st.columns(3)

    with f1:
        search_text = st.text_input("Search signals")

    with f2:
        categories = st.multiselect(
            "Categories",
            sorted(df["category"].dropna().astype(str).unique()),
            default=sorted(df["category"].dropna().astype(str).unique())
        )

    with f3:
        priorities = st.multiselect(
            "Priorities",
            sorted(df["priority"].dropna().astype(str).unique()),
            default=sorted(df["priority"].dropna().astype(str).unique())
        )

    f4, f5 = st.columns(2)

    with f4:
        sources = st.multiselect(
            "Sources",
            sorted(df["source"].dropna().astype(str).unique()),
            default=sorted(df["source"].dropna().astype(str).unique())
        )

    with f5:
        min_relevance = st.slider(
            "Minimum relevance score",
            0, 100, 0
        )

    filtered = df[
        df["category"].astype(str).isin(categories)
        & df["priority"].astype(str).isin(priorities)
        & df["source"].astype(str).isin(sources)
        & (df["relevance_score"] >= min_relevance)
    ].copy()

    if search_text.strip():
        mask = (
            filtered["title"].astype(str).str.contains(
                search_text, case=False, na=False
            )
            | filtered["content"].astype(str).str.contains(
                search_text, case=False, na=False
            )
        )
        filtered = filtered[mask]

    st.caption(f"Showing {len(filtered)} of {len(df)} signals")

    if filtered.empty:
        st.warning("No signals match the selected filters.")
        return

    records = filtered.to_dict("records")

    st.divider()

    # PRIORITY INTELLIGENCE
    st.header("⚡ Priority Intelligence")

    p1, p2 = st.columns(2)

    with p1:
        priority_data = filtered["priority"].value_counts().reset_index()
        priority_data.columns = ["Priority", "Count"]

        st.plotly_chart(
            px.bar(
                priority_data,
                x="Priority",
                y="Count",
                title="Priority Distribution"
            ),
            use_container_width=True
        )

    with p2:
        st.plotly_chart(
            px.histogram(
                filtered,
                x="priority_score",
                nbins=10,
                title="Priority Score Distribution"
            ),
            use_container_width=True
        )

    st.divider()

    # TREND INTELLIGENCE
    st.header("📈 Trend Intelligence")

    trend = generate_trend_report(records)

    t1, t2 = st.columns(2)

    keywords = safe_dataframe(trend.get("keywords", []))
    category_data = safe_dataframe(
        trend.get("category_distribution", [])
    )

    with t1:
        if not keywords.empty and len(keywords.columns) >= 2:
            st.plotly_chart(
                px.bar(
                    keywords,
                    x=keywords.columns[0],
                    y=keywords.columns[1],
                    title="Trending Keywords"
                ),
                use_container_width=True
            )
        else:
            st.info("No keyword trends available.")

    with t2:
        if not category_data.empty and len(category_data.columns) >= 2:
            st.plotly_chart(
                px.pie(
                    category_data,
                    names=category_data.columns[0],
                    values=category_data.columns[1],
                    title="Category Distribution"
                ),
                use_container_width=True
            )
        else:
            st.info("No category data available.")

    timeline = safe_dataframe(trend.get("timeline", []))

    if not timeline.empty and len(timeline.columns) >= 2:
        st.plotly_chart(
            px.line(
                timeline,
                x=timeline.columns[0],
                y=timeline.columns[1],
                title="Signal Activity Timeline",
                markers=True
            ),
            use_container_width=True
        )

    with st.expander("🔥 Rising Topics"):
        for topic in trend.get("rising_topics", []):
            st.write(f"• {topic}")

    st.divider()

    # COMPETITOR INTELLIGENCE
    st.header("🏢 Competitor Intelligence Center")

    competitor = analyze_competitors(records)

    competitor_events = safe_dataframe(
        competitor.get("event_distribution", [])
    )
    competitor_activities = safe_dataframe(
        competitor.get("activities", [])
    )
    competitor_names = competitor.get("competitor_names", [])

    c1, c2, c3 = st.columns(3)

    c1.metric("Competitor Signals", competitor.get("total_signals", 0))
    c2.metric("Competitors Identified", len(competitor_names))
    c3.metric("Activity Types", len(competitor_events))

    if not competitor_events.empty and len(competitor_events.columns) >= 2:
        st.plotly_chart(
            px.bar(
                competitor_events,
                x=competitor_events.columns[0],
                y=competitor_events.columns[1],
                title="Competitor Event Distribution"
            ),
            use_container_width=True
        )

    with st.expander("View Competitor Names"):
        st.write(competitor_names if competitor_names else "No names identified.")

    with st.expander("View Competitor Records"):
        st.dataframe(competitor_activities, use_container_width=True)

    st.divider()

    # CUSTOMER INTELLIGENCE
    st.header("👥 Customer Intelligence Center")

    customer = analyze_customers(records)

    customer_events = safe_dataframe(
        customer.get("event_distribution", [])
    )
    customer_sentiment = safe_dataframe(
        customer.get("sentiment_distribution", [])
    )
    customer_activities = safe_dataframe(
        customer.get("activities", [])
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Customer Signals", customer.get("total_signals", 0))
    c2.metric("Customer Event Types", len(customer_events))
    c3.metric("Sentiment Types", len(customer_sentiment))

    a, b = st.columns(2)

    with a:
        if not customer_sentiment.empty and len(customer_sentiment.columns) >= 2:
            st.plotly_chart(
                px.pie(
                    customer_sentiment,
                    names=customer_sentiment.columns[0],
                    values=customer_sentiment.columns[1],
                    title="Customer Sentiment"
                ),
                use_container_width=True
            )

    with b:
        if not customer_events.empty and len(customer_events.columns) >= 2:
            st.plotly_chart(
                px.bar(
                    customer_events,
                    x=customer_events.columns[0],
                    y=customer_events.columns[1],
                    title="Customer Event Distribution"
                ),
                use_container_width=True
            )

    with st.expander("View Customer Records"):
        st.dataframe(customer_activities, use_container_width=True)

    st.divider()

    # MARKET INTELLIGENCE
    st.header("🌍 Market Intelligence Center")

    market = analyze_market(records)

    market_events = safe_dataframe(
        market.get("event_distribution", [])
    )
    opportunities = safe_dataframe(
        market.get("opportunity_distribution", [])
    )
    risks = safe_dataframe(
        market.get("risk_distribution", [])
    )
    market_activities = safe_dataframe(
        market.get("activities", [])
    )

    m1, m2, m3 = st.columns(3)

    m1.metric("Market Signals", market.get("total_signals", 0))
    m2.metric(
        "Opportunity Types",
        market.get("total_opportunities", len(opportunities))
    )
    m3.metric(
        "Risk Types",
        market.get("total_risks", len(risks))
    )

    a, b = st.columns(2)

    with a:
        if not market_events.empty and len(market_events.columns) >= 2:
            st.plotly_chart(
                px.bar(
                    market_events,
                    x=market_events.columns[0],
                    y=market_events.columns[1],
                    title="Market Events"
                ),
                use_container_width=True
            )

    with b:
        if not opportunities.empty and len(opportunities.columns) >= 2:
            st.plotly_chart(
                px.bar(
                    opportunities,
                    x=opportunities.columns[0],
                    y=opportunities.columns[1],
                    title="Market Opportunities"
                ),
                use_container_width=True
            )

    if not risks.empty and len(risks.columns) >= 2:
        st.plotly_chart(
            px.bar(
                risks,
                x=risks.columns[0],
                y=risks.columns[1],
                title="Market Risks"
            ),
            use_container_width=True
        )

    with st.expander("View Market Records"):
        st.dataframe(market_activities, use_container_width=True)

    st.divider()

    # INTERNAL INTELLIGENCE
    st.header("🏭 Internal Intelligence Center")

    internal = analyze_internal(records)

    internal_events = safe_dataframe(
        internal.get("event_distribution", [])
    )

    internal_keywords = safe_dataframe(
        internal.get("keyword_distribution", [])
    )

    internal_activities = safe_dataframe(
        internal.get("activities", [])
    )

    i1, i2, i3 = st.columns(3)

    i1.metric("Internal Signals", internal.get("total_signals", 0))
    i2.metric("Detected Events", internal.get("total_events", 0))
    i3.metric("Event Types", len(internal_events))

    a, b = st.columns(2)

    with a:
        if not internal_events.empty:
            st.plotly_chart(
                px.bar(
                    internal_events,
                    x="event",
                    y="count",
                    title="Internal Event Distribution"
                ),
                use_container_width=True
            )
        else:
            st.info("No internal events detected.")

    with b:
        if not internal_keywords.empty:
            st.plotly_chart(
                px.bar(
                    internal_keywords.head(10),
                    x="keyword",
                    y="count",
                    title="Top Internal Keywords"
                ),
                use_container_width=True
            )
        else:
            st.info("No internal keywords detected.")

    with st.expander("View Internal Activity Records"):
        st.dataframe(internal_activities, use_container_width=True)

    st.divider()


    # EXECUTIVE INTELLIGENCE SUMMARY
    st.header("🧠 Executive Intelligence Summary")

    executive = generate_executive_summary(records)

    e1, e2, e3, e4 = st.columns(4)

    e1.metric("Total Signals", executive["total_signals"])
    e2.metric("Critical Signals", executive["total_critical"])
    e3.metric("Opportunities", executive["total_opportunities"])
    e4.metric("Detected Risks", executive["total_risks"])

    st.subheader("Business Intelligence by Category")

    executive_categories = safe_dataframe(
        executive.get("category_summary", [])
    )

    if not executive_categories.empty:
        st.plotly_chart(
            px.bar(
                executive_categories,
                x="category",
                y="signal_count",
                title="Intelligence Coverage by Category"
            ),
            use_container_width=True
        )
        st.dataframe(
            executive_categories,
            use_container_width=True
        )

    st.subheader("🚨 Critical Signals")

    critical_records = executive.get("critical_signals", [])

    if critical_records:
        for item in critical_records[:5]:
            st.warning(
                str(item.get("title", "Untitled"))
                + " — "
                + str(item.get("content", ""))[:250]
            )
    else:
        st.info("No critical signals identified.")

    st.subheader("💡 Business Opportunities")

    opportunity_records = executive.get("opportunities", [])

    if opportunity_records:
        for item in opportunity_records[:5]:
            st.write(
                "• "
                + str(item.get("title", "Untitled"))
            )
    else:
        st.info("No opportunity-related signals identified.")

    st.subheader("⚠️ Business Risks")

    risk_records = executive.get("risks", [])

    if risk_records:
        for item in risk_records[:5]:
            st.write(
                "• "
                + str(item.get("title", "Untitled"))
            )
    else:
        st.info("No risk-related signals identified.")

    st.subheader("🎯 Executive Recommendations")

    for index, recommendation in enumerate(
        executive.get("recommendations", []), start=1
    ):
        st.write(f"{index}. {recommendation}")

    st.divider()

    # TOP PRIORITY SIGNALS
    st.header("🚨 Top Priority Signals")

    top_signals = filtered.sort_values(
        "priority_score",
        ascending=False
    ).head(5)

    for _, signal in top_signals.iterrows():
        with st.expander(
            f"{signal['title']} — {signal['priority']}"
        ):
            st.write(signal["content"])
            st.write(f"Category: {signal['category']}")
            st.write(f"Priority Score: {signal['priority_score']}")
            st.write(f"Relevance Score: {signal['relevance_score']}")
            st.write(f"Source: {signal['source']}")

    # COMPLETE DATABASE
    st.header("🗂️ Complete Signal Database")
    st.dataframe(filtered, use_container_width=True)


render_dashboard()
