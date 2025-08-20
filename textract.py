import fitz  # PyMuPDF
import time
import os

def extract_pdf_all(file_path: str, output_dir: str = "pdf_output"):
    start_time = time.time()

    doc = fitz.open(file_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract metadata
    metadata = doc.metadata
    print("📄 PDF Metadata:", metadata)

    all_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract text
        text = page.get_text("text")
        all_text.append(text)

        # Extract images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"{output_dir}/page{page_num+1}_img{img_index}.{image_ext}"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)

    end_time = time.time()
    duration = end_time - start_time

    # Save text to file
    text_output_path = os.path.join(output_dir, "extracted_text.txt")
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print(f"✅ Extracted {len(all_text)} pages of text")
    print(f"🖼️ Extracted images saved in {output_dir}/")
    print(f"⏱️ Time taken: {duration:.2f} seconds")

    return {
        "metadata": metadata,
        "text_file": text_output_path,
        "output_dir": output_dir,
        "duration": duration
    }


if __name__ == "__main__":
    pdf_file = "/Users/devenpuri/Downloads/principia_newton.pdf"  # replace with your PDF path
    extract_pdf_all(pdf_file)
