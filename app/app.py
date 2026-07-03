import streamlit as st
from pathlib import Path
import os
import sys

# Centralized root configuration system setup
ROOT_PATH = str(Path(__file__).resolve().parent.parent)
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

from config.settings import Settings
from services.document_handler import DocumentHandler
from database.db_manager import DBManager
from services.vector_handler import VectorService
from services.quiz_engine import LLMService
from services.rag_engine import RAGEngine

# =====================================================================
# 1. Core Bootstrapping & Pre-flight Validation
# =====================================================================
Settings.initialize()
print(f"DEBUG: Settings.GEMINI_API_KEY = {Settings.GEMINI_API_KEY}")

def run_preflight_checks():
    """Validates configuration and file system access before booting the app."""
    # Re‑initialize settings to ensure env vars are loaded
    Settings.initialize()
    if not Settings.GEMINI_API_KEY:
        st.error("FATAL ERROR: GEMINI_API_KEY is missing or empty in .env.")
        st.stop()
    # Check write permissions on database directory
    try:
        test_file = Settings.DB_PATH.parent / ".write_test"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        st.error(f"FATAL ERROR: Cannot write to database directory: {e}")
        st.stop()

run_preflight_checks()

try:
    DBManager.init_db()
except Exception as e:
    print(f"FATAL ERROR: Database init failed: {e}")
    sys.exit(1)

# =====================================================================
# 2. Streamlit Page Configuration & Resource Initialization
# =====================================================================
st.set_page_config(page_title="EduGuide AI", page_icon="🎓", layout="wide")

@st.cache_resource
def init_services():
    """Initializes global backend boundaries and microservices frameworks."""
    # Ensure initialized in cached context as well
    Settings.initialize()
    return VectorService(), LLMService(), RAGEngine()

try:
    vector_service, llm_service, rag_engine = init_services()
except Exception as e:
    st.error(f"❌ Failed to boot core backend services: {e}")
    st.stop()

# Dashboard Title
st.title("🎓 EduGuide AI Mentorship Companion")
st.caption("Your intelligent RAG-driven learning and assessment workspace.")
st.markdown("---")

# =====================================================================
# 3. Sidebar: Document Ingestion Pipeline
# =====================================================================
st.sidebar.header("📁 Document Management")
uploaded_file = st.sidebar.file_uploader("Upload course material (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Ensure standard structural storage directories exist
    os.makedirs(Settings.UPLOADS_PATH, exist_ok=True)
    temp_pdf_path = Settings.UPLOADS_PATH / uploaded_file.name
    
    # Save file buffer to local disk stream
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Check if document already exists inside SQLite index catalog
    doc_record = DBManager.get_document_by_name(uploaded_file.name)
    
    if not doc_record:
        with st.sidebar.status("Executing document ingestion...", expanded=True) as status:
            st.write("⏳ Extracting text & Segmenting pages into isolated chunks...")
            chunks = DocumentHandler.process_and_chunk(str(temp_pdf_path))
            
            if chunks:
                st.write("⏳ Registering relational database schema maps...")
                doc_id = DBManager.register_document(
                    filename=uploaded_file.name,
                    file_path=str(temp_pdf_path),
                    chunk_count=len(chunks)
                )
                
                st.write("⏳ Vectorizing tokens & writing collections to index store...")
                vector_service.add_documents(chunks)
                status.update(label="Ingestion complete! 🎉", state="complete")
                st.sidebar.success(f"Successfully processed {uploaded_file.name} (Total Chunks: {len(chunks)})")
            else:
                status.update(label="Ingestion failed ❌", state="error")
                st.sidebar.error("Could not process PDF content. Check format limits.")
    else:
        st.sidebar.info(f"💡 Document context database cached for: '{uploaded_file.name}'")

# =====================================================================
# 4. Main Tab Interface
# =====================================================================
tab1, tab2, tab3 = st.tabs(["📄 Smart Summary & Q&A", "📝 Interactive Quiz", "📊 Performance Analytics"])

# ---------------------------------------------------------------------
# TAB 1: SMART SUMMARY & Q&A (RAG Core)
# ---------------------------------------------------------------------
with tab1:
    st.header("Smart Notebook Summary & Assistant")
    if uploaded_file is None:
        st.info("👋 Upload a study PDF from the side panel to generate core key-insights summary maps.")
    else:
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            if st.button("Generate Contextual Summary", type="primary", use_container_width=True):
                with st.spinner("Retrieving semantic points and drafting study notes..."):
                    # Vector search configuration mapping
                    results = vector_service.query_top_k("Summarize the core concepts and definitions", k=5)
                    context_text = "\n".join([item["text"] for item in results])
                    
                    if context_text:
                        summary_output = llm_service.summarize_text(context_text)
                        st.markdown("### 📝 Core Analytical Study Notes")
                        st.markdown(summary_output)
                    else:
                        st.error("Could not trace structural background content inside your vector index.")
        
        with col_right:
            st.markdown("#### 💬 Ask anything from this Document")
            user_query = st.text_input("Enter your question here...", placeholder="What is the main definition of...?")
            if user_query:
                with st.spinner("Searching document context & asking Gemini..."):
                    results = vector_service.query_top_k(user_query, k=3)
                    context_text = "\n".join([item["text"] for item in results])
                    rag_response = rag_engine.query(user_query, context_text)
                    st.info(rag_response)

# ---------------------------------------------------------------------
# TAB 2: INTERACTIVE PRACTICE QUIZ
# ---------------------------------------------------------------------
with tab2:
    st.header("Dynamic MCQ Assessment Center")
    if uploaded_file is None:
        st.info("👋 Upload course material to unlock randomized custom evaluation checks.")
    else:
        num_questions = st.slider("Target Question Count", min_value=3, max_value=10, value=5)
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        
        if st.button("Construct Live Custom Assessment", use_container_width=True):
            with st.spinner("Extracting balanced topical content and generating schema questions..."):
                results = vector_service.query_top_k("Generate conceptual evaluation multiple choice configurations", k=6)
                context_text = "\n".join([item["text"] for item in results])
                
                try:
                    st.session_state.quiz_pool = llm_service.generate_quiz(context_text, num_questions=num_questions, difficulty=difficulty)
                    st.session_state.quiz_submitted = False
                except Exception as e:
                    st.error(f"Quiz runtime process exception: {e}")
                    
        if "quiz_pool" in st.session_state and st.session_state.quiz_pool:
            st.write("---")
            user_selections = []
            doc_record = DBManager.get_document_by_name(uploaded_file.name)
            
            with st.form("assessment_form"):
                for idx, q in enumerate(st.session_state.quiz_pool):
                    st.markdown(f"**Q{idx+1}.** {q['question']}")
                    choice = st.radio(f"Options for Q{idx+1}", options=q['options'], key=f"form_q_{idx}")
                    user_selections.append(choice)
                    st.markdown("")
                    
                submitted = st.form_submit_button("Submit Answers for Verification", use_container_width=True)
                
                if submitted:
                    st.session_state.quiz_submitted = True
                    correct_count = 0
                    answers_log = []
                    
                    st.markdown("### 🎯 Live Test Review Summary:")
                    for idx, q in enumerate(st.session_state.quiz_pool):
                        is_correct = (user_selections[idx] == q['answer'])
                        if is_correct:
                            st.success(f"✔ **Question {idx+1}: Correct Selection!** -> *{user_selections[idx]}*")
                            correct_count += 1
                        else:
                            st.error(f"❌ **Question {idx+1}: Incorrect.** Expected: `{q['answer']}` | Selected: `{user_selections[idx]}`")
                        
                        answers_log.append({
                            "question_text": q["question"],
                            "selected_option": user_selections[idx],
                            "correct_option": q["answer"],
                            "is_correct": is_correct
                        })
                        
                    # Save performance history via SQLite transactional engine
                    if doc_record:
                        attempt_id = DBManager.record_quiz_attempt(
                            document_id=doc_record["id"],
                            score=correct_count,
                            total_questions=len(st.session_state.quiz_pool),
                            answers=answers_log
                        )
                        st.metric(label="Calculated Performance Accuracy Ratio", value=f"{correct_count} / {len(st.session_state.quiz_pool)}")
        elif "quiz_pool" in st.session_state:
            st.warning("⚠️ No questions could be generated. Try parsing a different section or adjust configurations.")

# ---------------------------------------------------------------------
# TAB 3: PERFORMANCE ANALYTICS
# ---------------------------------------------------------------------
with tab3:
    st.header("Learning Performance Metrics Tracker")
    analytics = DBManager.get_analytics_summary()
    history = DBManager.get_quiz_history()
    
    if analytics["total_attempts"] == 0:
        st.info("📉 No evaluations mapped into local SQLite. Complete your first practice test to track metrics.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Assessments Checked", analytics["total_attempts"])
        col2.metric("Mean Global Accuracy Score", f"{analytics['average_percentage']}%")
        col3.metric("Aggregated Correct Choices", f"{analytics['total_correct']} / {analytics['total_answered']}")
        
        # Chronological trend metrics
        if analytics["quiz_scores"]:
            st.subheader("📈 Historical Progress Curve")
            chart_scores = [item["percentage"] for item in analytics["quiz_scores"]]
            st.line_chart(chart_scores)
            
        st.subheader("📋 Relational Logging Logs (Top 5 Attempts)")
        for attempt in history[:5]:
            st.text(f"⏱ [{attempt['attempt_timestamp']}] File: {attempt['document_name']} | Raw Score: {attempt['score']}/{attempt['total_questions']}")