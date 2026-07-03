import os
import sys
from pathlib import Path
from dotenv import dotenv_values

# Robust Path Resolution
BASE_DIR = Path(__file__).resolve().parent.parent

# Discover .env file location
env_path_root = BASE_DIR / ".env"
env_path_config = BASE_DIR / "config" / ".env"

env_file_to_load = None
if env_path_root.is_file():
    env_file_to_load = env_path_root
elif env_path_config.is_file():
    env_file_to_load = env_path_config

# Load directly into memory dictionary to avoid Streamlit cache-pollution
print(f"DEBUG: BASE_DIR = {BASE_DIR}")
print(f"DEBUG: env_path_root exists? {env_path_root.is_file()}")
print(f"DEBUG: env_path_config exists? {env_path_config.is_file()}")
print(f"DEBUG: env_file_to_load = {env_file_to_load}")
env_vars = dotenv_values(env_file_to_load) if env_file_to_load else {}
print(f"DEBUG: env_vars = {env_vars}")

class Settings:
    # Project Paths
    PROJECT_ROOT = BASE_DIR
    UPLOADS_PATH = BASE_DIR / "docs"
    DB_PATH = BASE_DIR / "database" / "eduguide.db"
    CHROMA_PATH = BASE_DIR / "database" / "chroma_db"
    
    # Text Chunking Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # API Configurations
    GEMINI_API_KEY = None
    
    @classmethod
    def initialize(cls):
        """Ensure directories exist and initialize variables."""
        os.makedirs(cls.UPLOADS_PATH, exist_ok=True)
        os.makedirs(cls.DB_PATH.parent, exist_ok=True)
        os.makedirs(cls.CHROMA_PATH, exist_ok=True)
        
        # Rigorous API Key Loading (Env file takes priority over OS environment)
        cls.GEMINI_API_KEY = env_vars.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not cls.GEMINI_API_KEY:
            print(" WARNING: GEMINI_API_KEY not found in .env file or system environment!")