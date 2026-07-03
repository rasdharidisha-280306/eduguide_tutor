import os
import sqlite3

class DatabaseManager:
    """Helper manager to manage SQLite database transactions for user logs, quiz histories, and sessions."""
    
    def __init__(self, db_path: str = "database/eduguide.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self):
        """Returns a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table to store user quiz histories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    topic TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL
                )
            """)
            
            # Table to store search query history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL
                )
            """)
            conn.commit()

    def log_quiz_score(self, topic: str, score: int, total_questions: int):
        """Logs a quiz result to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO quiz_scores (topic, score, total_questions) VALUES (?, ?, ?)",
                (topic, score, total_questions)
            )
            conn.commit()

    def get_quiz_scores(self) -> list:
        """Retrieves all quiz score logs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, topic, score, total_questions FROM quiz_scores ORDER BY timestamp DESC")
            return cursor.fetchall()

    def log_query(self, query: str, response: str):
        """Logs a user query and its RAG engine response."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO query_history (query, response) VALUES (?, ?)",
                (query, response)
            )
            conn.commit()
            
    def get_query_history(self) -> list:
        """Retrieves all query history records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, query, response FROM query_history ORDER BY timestamp DESC")
            return cursor.fetchall()
