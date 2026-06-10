import pyttsx3
import sys
import os
import re
from pydub import AudioSegment
import tempfile
from tqdm import tqdm

# Note: Requires pip install pyttsx3 pydub tqdm
# For MP3 export, install ffmpeg: https://ffmpeg.org/download.html (add to PATH)

# Step 1: Read text from TXT file
def read_text_from_file(txt_path):
    text = ""
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            text = file.read()
            # Replace single newlines with spaces, preserve paragraph breaks
            cleaned_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
            text = cleaned_text
        # Normalize multiple spaces, keep paragraphs
        text = re.sub(r' +', ' ', text).strip()
        # Replace paragraph breaks with single space for TTS
        text = re.sub(r'\n+', ' ', text).strip()
        return text
    except UnicodeDecodeError:
        print("Error: Unable to decode the text file. Please ensure it's a valid UTF-8 encoded text file.")
        return None
    except Exception as e:
        print(f"Read error: {e}")
        return None

# Function to chunk text at word boundaries
def get_chunks(s, max_length=4000):
    """
    Split text into chunks of max_length characters, splitting at spaces to avoid mid-word cuts.
    """
    chunks = []
    start = 0
    while start < len(s):
        end = start + max_length
        if end >= len(s):
            chunks.append(s[start:])
            break
        # Find the last space before or at end
        last_space = s.rfind(' ', start, end + 1)
        if last_space == -1:
            # No space, take up to end
            chunks.append(s[start:end])
            start = end
            continue
        chunks.append(s[start:last_space])
        start = last_space + 1
    return chunks

# Step 2: Convert text chunk to WAV
def text_chunk_to_wav(text_chunk, wav_path):
    try:
        engine = pyttsx3.init()  # Auto-detect driver
        # Adjust voice settings
        engine.setProperty("rate", 200)  # Speed (words per minute)
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)
        else:
            engine.setProperty("voice", voices[0].id)
        
        # Save to WAV
        engine.save_to_file(text_chunk, wav_path)
        engine.runAndWait()
        engine.stop()
        return True
    except Exception as e:
        print(f"Error during text-to-speech conversion for chunk: {str(e)}")
        return False

# Step 3: Merge WAV files into MP3
def merge_wavs_to_mp3(wav_files, mp3_path):
    try:
        combined = AudioSegment.empty()
        for wav_file in tqdm(wav_files, desc="Merging audio files", unit="file", colour="yellow"):
            audio = AudioSegment.from_wav(wav_file)
            combined += audio
        print("Encoding final MP3 (this may take a while for large files)...")
        combined.export(mp3_path, format="mp3", bitrate="128k", parameters=["-preset", "fast"])
        return True
    except Exception as e:
        print(f"Error merging audio files: {str(e)}")
        return False

# Step 4: Convert text to MP3 with overall progress bar
def text_to_mp3(text, output_path):
    # Split into chunks
    chunks = get_chunks(text, max_length=4000)
    print(f"Split into {len(chunks)} chunks")
    
    total_steps = len(chunks) + 1  # Chunks + final MP3 export
    with tqdm(total=total_steps, desc="Overall progress", unit="step", colour="yellow") as pbar:
        wav_files = []
        base_dir = os.path.dirname(output_path) or '.'
        with tempfile.TemporaryDirectory() as temp_dir:
            # Process chunks
            for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks", unit="chunk", colour="yellow")):
                if not chunk.strip():
                    continue
                wav_filename = os.path.join(temp_dir, f"chunk_{i}.wav")
                if text_chunk_to_wav(chunk, wav_filename):
                    if os.path.exists(wav_filename) and os.path.getsize(wav_filename) > 100:  # Minimal check
                        wav_files.append(wav_filename)
                    else:
                        print(f"Warning: Chunk {i} WAV file is empty or too small.")
                else:
                    print(f"Failed to convert chunk {i}")
                    return False
                pbar.update(1)  # Update overall progress for each chunk
            
            if not wav_files:
                print("No valid audio chunks generated.")
                return False
            
            # Merge to MP3
            if merge_wavs_to_mp3(wav_files, output_path):
                pbar.update(1)  # Update overall progress for MP3 merge
                return True
            return False

# Run the process
if __name__ == "__main__":
    # Check if TXT path is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/your/text_file.txt")
        sys.exit(1)

    # Get TXT path from command line
    txt_path = sys.argv[1]

    # Ensure the file exists and is a .txt file
    if not os.path.isfile(txt_path) or not txt_path.lower().endswith('.txt'):
        print(f"Error: File '{txt_path}' does not exist or is not a .txt file.")
        sys.exit(1)

    # Generate MP3 path in the same directory as TXT
    mp3_path = os.path.splitext(txt_path)[0] + ".mp3"

    # Read text
    full_text = read_text_from_file(txt_path)
    if not full_text:
        print("Failed to read text from TXT file or file is empty.")
        sys.exit(1)

    print(f"Text length: {len(full_text)} characters")

    # Convert with progress bar
    if text_to_mp3(full_text, mp3_path):
        # Verify the output file
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1024:
            print(f"Conversion complete! MP3 saved as {mp3_path}")
        else:
            print(f"Error: MP3 file '{mp3_path}' was created but is too small or invalid.")
            sys.exit(1)
    else:
        print("Failed to convert text to MP3.")
        sys.exit(1)