#!/bin/bash

# Start Streamlit GUI for DigiMarket API Testing
# This script starts the Streamlit web interface for testing the API

echo "🛒 Starting DigiMarket API Tester..."
echo ""
echo "Make sure the API server is running on http://localhost:5001"
echo "If not, start it with: python run.py"
echo ""
echo "Starting Streamlit GUI..."
echo "The GUI will open in your browser at http://localhost:8501"
echo ""

streamlit run streamlit_app.py
