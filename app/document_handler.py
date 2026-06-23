import fitz  
# PyMuPDF library

def parse_pdf(pdf_path):
    try:
        # opens pdf file
        doc = fitz.open(pdf_path)
        parsed_data = []
        
        # extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # saving page number and text in a dictionary
            parsed_data.append({
                "page": page_num + 1,
                "text": text
            })
            
        return parsed_data
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
   
    pdf_name = "docs/sample.pdf"
    
    print("PDF parsing shuru ho rahi hai...")
    result = parse_pdf(pdf_name)
    
    if result:
        print(f"\n✅ Success! Total {len(result)} pages parsed.")
        print("\n--- sample text for page 1 ---")
        print(result[0]["text"][:300])  