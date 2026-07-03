import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import Settings
from database.db_manager import DBManager

def verify():
    print("🚀 Starting Setup Verification...")
    
    # 1. Verify Configuration & Environment Variables
    print("\n[1] Verifying Environment Configurations...")
    Settings.initialize()
    if Settings.GEMINI_API_KEY:
        print("✅ GEMINI_API_KEY is successfully configured and loaded.")
    else:
        print("❌ ERROR: GEMINI_API_KEY is missing. Check your .env file.")
        sys.exit(1)
        
    # 2. Verify Database Schema
    print("\n[2] Verifying SQLite Database...")
    try:
        DBManager.init_db()
        print("✅ Database tables successfully verified without OperationalError.")
    except Exception as e:
        print(f"❌ ERROR: Database initialization failed: {e}")
        sys.exit(1)
        
    print("\n🎉 All checks passed! You can now run the Streamlit app safely.")
    print("   Run: streamlit run app/app.py")

if __name__ == "__main__":
    verify()
