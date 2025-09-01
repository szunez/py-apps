import PyPDF2
import re
import sys
import os
import glob

# Step 1: Extract text from PDF and write to text file
def extract_text_from_pdf(pdf_path, output_txt_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    # Replace single newlines with spaces, keep double newlines for paragraphs
                    cleaned_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', page_text)
                    text += cleaned_text + "\n\n"  # Add double newline between pages
        
        # Normalize multiple spaces and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Write the extracted text to the output file
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        
        return text
    except FileNotFoundError:
        return f"Error: The file {pdf_path} was not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the process
if __name__ == "__main__":
    # Check if at least one argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/pdf_file_pattern", file=sys.stderr)
        sys.exit(1)

    # Get PDF pattern from command line
    pdf_pattern = sys.argv[1]

    # Find all PDF files matching the pattern
    pdf_files = glob.glob(pdf_pattern)
    
    if not pdf_files:
        print(f"Error: No PDF files found matching '{pdf_pattern}'.", file=sys.stderr)
        sys.exit(1)

    # Process each PDF file
    for pdf_path in pdf_files:
        # Ensure the PDF file exists
        if not os.path.isfile(pdf_path):
            print(f"Error: File '{pdf_path}' does not exist.", file=sys.stderr)
            continue

        # Generate output text file path
        txt_path = os.path.splitext(pdf_path)[0] + ".txt"

        # Extract text
        extracted_text = extract_text_from_pdf(pdf_path, txt_path)
        
        if not extracted_text.startswith("Error"):
            print(f"Text successfully extracted from {pdf_path} to {txt_path}")
        else:
            print(extracted_text, file=sys.stderr)