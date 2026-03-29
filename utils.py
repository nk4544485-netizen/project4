import streamlit as st
import sqlite3
import os
import pandas as pd

# Define the absolute Base Directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "phonepe_pulse.db")

def format_currency(num):
    if num >= 1e7:
        return f"₹{num/1e7:.2f} Cr"
    elif num >= 1e5:
        return f"₹{num/1e5:.2f} L"
    else:
        return f"₹{num:,.2f}"

def format_count(num):
    if num >= 1e7:
        return f"{num/1e7:.2f} Cr"
    elif num >= 1e5:
        return f"{num/1e5:.2f} L"
    else:
        return f"{num:,}"

def get_db_connection():
    if not os.path.exists(DB_PATH):
        # Trigger mock data generation if real DB is missing
        try:
            from generate_mock_data import create_mock_db
            create_mock_db()
        except ImportError:
             st.error("Mock data generator script not found.")
             st.stop()
    
    return sqlite3.connect(DB_PATH, check_same_thread=False)
