import subprocess
import argparse
from pathlib import Path

def convert_djvu_to_pdf(input_file, output_file):
    try:
        subprocess.run(["ddjvu", "-format=pdf", input_file, output_file], check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert a DJVU file to PDF")
    parser.add_argument("input_file", help="Path to the input DJVU file")
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = input_path.with_suffix('.pdf')
    
    convert_djvu_to_pdf(str(input_path), str(output_path))

if __name__ == "__main__":
    main()