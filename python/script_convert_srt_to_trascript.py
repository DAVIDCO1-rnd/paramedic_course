import os
import re

def convert_srt_to_transcript(srt_file_full_path):
    """
    Converts an .srt subtitles file into a plain text transcript
    containing only unique text lines (no repeats), preserving line breaks.
    """
    import os
    import re

    if not os.path.exists(srt_file_full_path):
        raise FileNotFoundError(f"File not found: {srt_file_full_path}")

    # Read the file
    with open(srt_file_full_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Remove index and timestamp lines
    cleaned = re.sub(r"\d+\s*\n\d{2}:\d{2}:\d{2},\d{3} --> .*?\n", "", content)
    cleaned = re.sub(r"^\d+\s*$", "", cleaned, flags=re.MULTILINE)

    # Split into non-empty lines
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]

    # Remove consecutive duplicate lines
    transcript_lines = []
    prev_line = None
    for line in lines:
        if line != prev_line:
            transcript_lines.append(line)
            prev_line = line

    # Join with line breaks
    transcript_text = "\n".join(transcript_lines)

    # Save to a text file
    output_file = os.path.splitext(srt_file_full_path)[0] + "_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print(f"Transcript saved to: {output_file}")
    return output_file


def main():
    current_folder_full_path = os.getcwd()
    parent_folder_full_path = os.path.dirname(current_folder_full_path)
    subfolder_name = 'advanced_emt'
    subfolder_full_path = os.path.join(parent_folder_full_path, subfolder_name)
    srt_name = 'cardiac_arrhythmias_Tomy_Kwit.srt'
    srt_file_full_path = os.path.join(subfolder_full_path, srt_name)
    transcript_text_full_path = convert_srt_to_transcript(srt_file_full_path)

main()
