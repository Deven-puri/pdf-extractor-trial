from tika import parser
import fitz  # PyMuPDF
import time
import os

def extract_pdf_all(file_path: str, image_output_dir: str = "extracted_images"):
    start_time = time.time()

    
    parsed = parser.from_file(file_path)
    text = parsed.get("content", "")
    metadata = parsed.get("metadata", {})

    
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)

    image_count = 0
    with fitz.open(file_path) as doc:
        for page_index, page in enumerate(doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                image_count += 1
                img_filename = os.path.join(image_output_dir, f"page{page_index+1}_img{img_index+1}.png")

                if pix.n < 5:  # GRAY or RGB
                    pix.save(img_filename)
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(img_filename)
                    pix1 = None
                pix = None

    end_time = time.time()
    duration = end_time - start_time

    print("✅ PDF Extraction Complete")
    print(f"📄 Characters Extracted: {len(text) if text else 0}")
    print(f"📑 Metadata Keys: {list(metadata.keys())}")
    print(f"🖼️ Images Extracted: {image_count} (saved in '{image_output_dir}/')")
    print(f"⏱️ Time Taken: {duration:.2f} seconds")

    return {
        "text": text,
        "metadata": metadata,
        "images_extracted": image_count,
        "duration": duration
    }


if __name__ == "__main__":
    pdf_file = "/Users/devenpuri/Downloads/principia_newton.pdf"  
    result = extract_pdf_all(pdf_file)

    
    print("\n🔎 Text Preview:\n", result["text"][:500], "...\n")
