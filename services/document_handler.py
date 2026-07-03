import fitz  # PyMuPDF
import os
import re
from config.settings import Settings

class DocumentHandler:
    """Handles parsing PDFs, extraction of raw clean text arrays, and structural structural chunk splitting."""
    
    @classmethod
    def process_and_chunk(cls, pdf_path: str) -> list:
        """Parses a local PDF resource file path and breaks it down into granular structured chunks."""
        try:
            doc = fitz.open(pdf_path)
            raw_chunks = []
            
            # 1. Sequential Page Text Ingestion Loop
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                
                # Context cleaning syntax regex structures
                text = re.sub(r'\s+', ' ', text).strip()
                if not text:
                    continue
                    
                # 2. Text Splitting Allocation by Threshold Values
                # Settings chunk structure window configs mapping
                chunk_size = Settings.CHUNK_SIZE
                overlap = Settings.CHUNK_OVERLAP
                
                start = 0
                while start < len(text):
                    end = start + chunk_size
                    chunk_text = text[start:end]
                    
                    raw_chunks.append({
                        "text": chunk_text,
                        "metadata": {
                            "source": os.path.basename(pdf_path),
                            "page": page_num + 1
                        }
                    })
                    # Calculation of window sliding overlay boundaries
                    start += (chunk_size - overlap)
                    
            return raw_chunks
            
        except Exception as e:
            print(f"❌ Critical Exception triggered inside DocumentHandler parsing pipeline: {e}")
            return []

if __name__ == "__main__":
    # Internal test diagnostic configuration routine
    test_pdf = os.path.join(Settings.PROJECT_ROOT, "docs", "sample.pdf")
    print("🔬 Launching isolated pipeline verification routines...")
    chunks = DocumentHandler.process_and_chunk(test_pdf)
    print(f"✅ Executed. Total generated atomic elements cataloged: {len(chunks)}")