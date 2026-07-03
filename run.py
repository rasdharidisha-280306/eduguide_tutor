import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting EduGuide AI Mentorship Companion...")
    
    # Ensure standard files exist
    env_file = Path("config/.env")
    env_example = Path("config/.env.example")
    
    if not env_file.exists():
        print("\n⚠️  Warning: config/.env file not found!")
        if env_example.exists():
            print("💡 Creating config/.env from config/.env.example template.")
            try:
                env_file.write_text(env_example.read_text())
                print("✅ Created config/.env. Please open it and add your GEMINI_API_KEY.")
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
        else:
            print("❌ config/.env.example not found. Please create a config/.env file manually.")
    
    # Run Streamlit
    print("\n🖥️  Launching Streamlit application...")
    try:
        # Use subprocess to run streamlit
        subprocess.run(["streamlit", "run", "app/app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 EduGuide AI stopped.")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        print("💡 Make sure streamlit is installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
