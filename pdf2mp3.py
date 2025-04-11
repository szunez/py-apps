import PyPDF2
import pyttsx3
import sys
import os

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "  # Add space between pages
    return text

# Step 2: Convert text to MP3
def text_to_mp3(text, output_path):
    engine = pyttsx3.init()
    # Optional: Adjust voice settings
    engine.setProperty("rate", 300)  # Speed (words per minute)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # Change index for different voices
    # Save to MP3
    engine.save_to_file(text, output_path)
    engine.runAndWait()

# Run the process
if __name__ == "__main__":
    # Check if PDF path is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/your/pdf_file.pdf")
        sys.exit(1)

    # Get PDF path from command line
    pdf_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist.")
        sys.exit(1)

    # Generate MP3 path in the same directory as PDF
    mp3_path = os.path.splitext(pdf_path)[0] + ".mp3"

    # Extract and convert
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        text_to_mp3(extracted_text, mp3_path)
        print(f"Conversion complete! MP3 saved as {mp3_path}")
    else:
        print("Failed to extract text from PDF.")