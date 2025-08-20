import textract
import time

def parse_pdf_with_textract(file_path: str):
    start_time = time.time()

    text = textract.process(file_path, method="pdftotext")  
    end_time = time.time()

    duration = end_time - start_time
    num_chars = len(text.decode("utf-8"))

    print(f"✅ Extracted {num_chars} characters")
    print(f"⏱️ Time taken: {duration:.2f} seconds")

    return duration


if __name__ == "__main__":
    pdf_file = "/Users/devenpuri/Downloads/principia_newton.pdf"  
    parse_pdf_with_textract(pdf_file)
