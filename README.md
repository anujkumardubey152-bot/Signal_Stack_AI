# 📊 Signal Stack AI
### Intelligent Business Signal Monitoring and Analysis System

Signal Stack AI is a Python-based business intelligence dashboard designed to organise, classify, prioritise, and analyse business-related information.

It brings signals from different business areas into one dashboard, helping users understand customer feedback, competitor activities, market developments, and internal updates.

The project focuses on transforming scattered business information into structured insights through classification, relevance scoring, prioritisation, trend analysis, and executive summaries.

<p align="center">

**Live Application:** https://signalstackai.streamlit.app/

**GitHub Repository:** https://github.com/anujkumardubey152-bot/Signal_Stack_AI

</p>

---

## 🚀 Project Overview

Businesses receive information from multiple sources every day. Reviewing these updates manually can make it difficult to identify important developments and decide what deserves attention.

Signal Stack AI provides a centralised dashboard where users can submit business signals and analyse them through a modular processing pipeline.

The system currently uses rule-based and keyword-based analysis to organise information and generate initial business intelligence insights.

## ✨ Key Features

### 1. Business Signal Classification
Automatically categorises submitted signals into four categories:

- 👥 Customers
- 🏢 Competitors
- 📈 Market
- ⚙️ Internal

### 2. Relevance Scoring
Assigns relevance scores to submitted signals to help identify information that may be important to the business.

### 3. Priority Analysis
Calculates priority scores to help organise signals according to their importance.

### 4. Duplicate Detection
Uses content hashing to identify duplicate signal submissions and prevent identical records from being stored repeatedly.

### 5. Trend Analysis
Analyses keywords and signal dates to provide an overview of frequently occurring topics and activity over time.

### 6. Competitor Intelligence
Organises competitor-related information and identifies activities such as product launches and technology developments.

### 7. Customer Intelligence
Analyses customer-related signals, including feedback and complaints, using rule-based indicators.

### 8. Market Intelligence
Organises market-related signals and identifies potential opportunities and risks through predefined analysis rules.

### 9. Internal Intelligence
Processes internal business updates and categorises operational information.

### 10. Executive Summary
Combines available signals, category distributions, priority information, and recommendations into a consolidated dashboard view.

---

## 🏗️ System Architecture

The application follows a modular processing architecture.

```text
              BUSINESS SIGNAL INPUT
                       |
                       v
              SIGNAL PROCESSING
                       |
                       v
              CLASSIFICATION
                       |
                       v
              RELEVANCE SCORING
                       |
                       v
              PRIORITY ANALYSIS
                       |
                       v
              DUPLICATE DETECTION
                       |
                       v
                SQLITE DATABASE
                       |
          +------------+------------+
          |            |            |
          v            v            v
       CUSTOMER    COMPETITOR     MARKET
       ANALYSIS     ANALYSIS     ANALYSIS
          |            |            |
          +------------+------------+
                       |
                       v
               TREND ANALYSIS
                       |
                       v
              EXECUTIVE SUMMARY
                       |
                       v
               STREAMLIT DASHBOARD
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Plotly | Data visualisation |
| SQLite | Database storage |
| Hashlib | Duplicate detection |
| GitHub | Version control and source hosting |
| Streamlit Community Cloud | Deployment |

## 📁 Project Structure

```text
Signal_Stack_AI/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
│
└── modules/
    ├── __init__.py
    ├── classifier.py
    ├── database.py
    ├── pipeline.py
    ├── dashboard.py
    ├── prioritizer.py
    ├── trend_analyzer.py
    ├── competitor_analyzer.py
    ├── customer_analyzer.py
    ├── market_analyzer.py
    ├── internal_analyzer.py
    └── executive_summary.py
```

## ⚙️ Installation and Setup

Follow these steps to run Signal Stack AI locally.

### Step 1: Clone the repository

```bash
git clone https://github.com/anujkumardubey152-bot/Signal_Stack_AI.git
```

### Step 2: Open the project directory

```bash
cd Signal_Stack_AI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 📊 How to Use

1. Open the deployed application.
2. Enter a business signal title.
3. Add its description or relevant information.
4. Enter the source of the signal.
5. Submit the signal.
6. Explore the assigned category, relevance score, and priority information.
7. Review the dashboard visualisations and available intelligence reports.
8. Explore the executive summary.

## 🧪 Example Business Signals

You can use sample inputs like these to explore the classification workflow.

| Category | Example Signal |
|---|---|
| Competitors | Competitor launches a new AI-powered product |
| Customers | Customers report difficulty using an AI platform |
| Market | Growing demand for AI automation in healthcare |
| Internal | Internal AI infrastructure upgrade completed |

These are example test inputs, not claims about real-world business events.

## 🔍 Current Implementation and Limitations

Signal Stack AI is an initial business intelligence prototype.

The current version uses keyword matching, predefined rules, scoring logic, and SQLite-based storage.

Some capabilities require further development:

- Live collection of external business signals.
- Advanced NLP and machine-learning-based classification.
- More accurate company and competitor entity extraction.
- Advanced sentiment analysis.
- Persistent cloud database storage.
- Automated alerts and scheduled intelligence reports.

**Storage note:** The deployed version currently uses a temporary SQLite database at `/tmp/signal_stack_ai.db`. Records may be lost when the application restarts or is redeployed. It should not be treated as permanent cloud storage.

## 🔮 Future Improvements

- Integrate live news and business data sources.
- Introduce advanced NLP and machine-learning models.
- Improve competitor and company name extraction.
- Add persistent cloud database support.
- Develop automated business intelligence alerts.
- Improve executive reporting and data visualisation.
- Introduce authentication and role-based access.

## 💰 Cost Statement

The project was developed using Python and free-tier development and deployment services.

| Resource | Cost |
|---|---:|
| Python | ₹0 |
| Google Colab Free | ₹0 |
| GitHub | ₹0 |
| Streamlit | ₹0 |
| Streamlit Community Cloud Free Tier | ₹0 |
| SQLite | ₹0 |
| **Total direct software and hosting cost** | **₹0** |

This estimate excludes internet, electricity, and hardware expenses. Free-tier services may have usage limits.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Python application development.
- Modular software architecture.
- Data processing and classification.
- Rule-based scoring and prioritisation.
- SQLite database integration.
- Duplicate detection using hashing.
- Data visualisation with Plotly.
- Building interactive applications with Streamlit.
- Version control and cloud deployment.

## 👨‍💻 Developer

**Anuj Kumar Dubey**

B.Tech Computer Science Student | IERT Prayagraj

Interested in Artificial Intelligence, Machine Learning, Data Science, and Generative AI.

**GitHub:** https://github.com/anujkumardubey152-bot

---

## 📌 Project Links

- 🌐 **Live Application:** https://signalstackai.streamlit.app/
- 💻 **Source Code:** https://github.com/anujkumardubey152-bot/Signal_Stack_AI

---

*Signal Stack AI — Turning scattered business signals into structured intelligence.*
