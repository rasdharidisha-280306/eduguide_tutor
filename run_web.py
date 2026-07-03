import os
import sys
from pathlib import Path
import subprocess

if __name__ == "__main__":
    # Ensure project root is in Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    print("🚀 Booting EduGuide AI Web Dashboard...")
    # Trigger streamlit run explicitly from the root directory context
    try:
        subprocess.run(["streamlit", "run", "app/app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Web Dashboard stopped.")