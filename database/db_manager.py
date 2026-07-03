import sqlite3
import logging
from typing import List, Dict, Any, Optional
from config.settings import Settings

logger = logging.getLogger(__name__)

class DBManager:
    @staticmethod
    def get_connection() -> sqlite3.Connection:
        conn = sqlite3.connect(str(Settings.DB_PATH), check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls) -> None:
        """Forces creation of tables. Validates schema and recreates if mismatched."""
        sql_statements = [
            "CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL UNIQUE, file_path TEXT NOT NULL, chunk_count INTEGER NOT NULL, upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);",
            "CREATE TABLE IF NOT EXISTS quiz_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, score INTEGER NOT NULL, total_questions INTEGER NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE SET NULL);",
            "CREATE TABLE IF NOT EXISTS quiz_answers (id INTEGER PRIMARY KEY AUTOINCREMENT, attempt_id INTEGER NOT NULL, question_text TEXT NOT NULL, selected_option TEXT NOT NULL, correct_option TEXT NOT NULL, is_correct BOOLEAN NOT NULL, FOREIGN KEY (attempt_id) REFERENCES quiz_attempts (id) ON DELETE CASCADE);"
        ]
        
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()
            
            # Validation logic to ensure schema isn't outdated (e.g., missing 'timestamp')
            try:
                cursor.execute("SELECT timestamp FROM quiz_attempts LIMIT 1")
            except sqlite3.OperationalError:
                logger.warning("Database schema mismatch detected (missing columns). Rebuilding tables...")
                cursor.execute("DROP TABLE IF EXISTS quiz_answers")
                cursor.execute("DROP TABLE IF EXISTS quiz_attempts")
                cursor.execute("DROP TABLE IF EXISTS documents")
                conn.commit()
                # Re-run creations
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
                
            print("Database tables verified/created successfully.")
        except sqlite3.Error as e:
            print(f"Error initializing DB: {e}")
            raise e
        finally:
            conn.close()

    @classmethod
    def get_document_by_name(cls, filename: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE filename = ?", (filename,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @classmethod
    def register_document(cls, filename: str, file_path: str, chunk_count: int) -> int:
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documents (filename, file_path, chunk_count) VALUES (?, ?, ?)",
                (filename, file_path, chunk_count)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def record_quiz_attempt(cls, document_id: int, score: int, total_questions: int, answers: List[Dict[str, Any]]) -> int:
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO quiz_attempts (document_id, score, total_questions) VALUES (?, ?, ?)",
                (document_id, score, total_questions)
            )
            attempt_id = cursor.lastrowid
            
            for ans in answers:
                cursor.execute(
                    "INSERT INTO quiz_answers (attempt_id, question_text, selected_option, correct_option, is_correct) VALUES (?, ?, ?, ?, ?)",
                    (attempt_id, ans["question_text"], ans["selected_option"], ans["correct_option"], ans["is_correct"])
                )
            conn.commit()
            return attempt_id
        finally:
            conn.close()

    @classmethod
    def get_analytics_summary(cls) -> Dict[str, Any]:
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total, SUM(score) as sum_score, SUM(total_questions) as sum_questions FROM quiz_attempts")
            row = cursor.fetchone()
            
            total_attempts = row["total"] or 0
            total_correct = row["sum_score"] or 0
            total_answered = row["sum_questions"] or 0
            
            avg = round((total_correct / total_answered * 100), 2) if total_answered > 0 else 0
            
            cursor.execute("SELECT score * 100.0 / total_questions as percentage FROM quiz_attempts ORDER BY timestamp ASC")
            scores = [{"percentage": r["percentage"]} for r in cursor.fetchall()]
            
            return {
                "total_attempts": total_attempts,
                "total_correct": total_correct,
                "total_answered": total_answered,
                "average_percentage": avg,
                "quiz_scores": scores
            }
        finally:
            conn.close()

    @classmethod
    def get_quiz_history(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT qa.id, qa.score, qa.total_questions, qa.timestamp as attempt_timestamp, d.filename as document_name 
                FROM quiz_attempts qa 
                LEFT JOIN documents d ON qa.document_id = d.id 
                ORDER BY qa.timestamp DESC
            ''')
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()