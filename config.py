
"""
Signal Stack AI
Application configuration.
Compatible with Google Colab and Streamlit Cloud.
"""

from pathlib import Path
import tempfile

PROJECT_NAME = "Signal Stack AI"

# Project directory: repository root
PROJECT_PATH = Path(__file__).resolve().parent

# Writable application data directory
DATA_PATH = Path(tempfile.gettempdir()) / "signal_stack_ai"
DATA_PATH.mkdir(parents=True, exist_ok=True)

# Database location
DATABASE_PATH = DATA_PATH / "signal_stack.db"

COMPANY_NAME = "MeetUniversity"

COMPANY_WEBSITE = "https://www.meetuniversity.com"

INTELLIGENCE_CATEGORIES = [
    "Customers",
    "Competitors",
    "Market",
    "Internal"
]

BRIEF_FREQUENCY = "Weekly"
