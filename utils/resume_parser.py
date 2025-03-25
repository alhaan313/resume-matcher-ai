import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_input):
    """Extracts text from a PDF file."""
    if isinstance(pdf_input, str):  # If input is a file path
        doc = fitz.open(pdf_input)
    else:  # If input is a file object
        pdf_input.seek(0)
        doc = fitz.open(stream=pdf_input.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in doc)
    return text.strip() if text else "No text extracted"


# Text value --> new_text_value --> 