import pdfplumber
import re
import os

def is_hebrew(char):
    return '\u0590' <= char <= '\u05FF'

def is_hebrew_word(word):
    return any(is_hebrew(c) for c in word)

def fix_brackets(text):
    # Swap left and right brackets to match RTL context
    bracket_map = str.maketrans("()[]{}", ")(][}{")
    return text.translate(bracket_map)

def fix_line_direction(line):
    tokens = re.split(r'(\s+)', line)  # Split by whitespace but keep the separators
    reversed_tokens = [
        fix_brackets(token[::-1]) if is_hebrew_word(token) else token
        for token in tokens
    ]

    # Count Hebrew words (not including whitespace)
    word_tokens = [t for t in reversed_tokens if not re.match(r'\s+', t)]
    hebrew_word_count = sum(1 for t in word_tokens if is_hebrew_word(t))

    if len(word_tokens) > 0 and hebrew_word_count >= len(word_tokens) / 2:
        # Mostly Hebrew: reverse word order
        words = []
        spaces = []
        for t in reversed_tokens:
            if re.match(r'\s+', t):
                spaces.append(t)
            else:
                words.append(t)
        words = list(reversed(words))
        result = []
        word_idx = 0
        for t in reversed_tokens:
            if re.match(r'\s+', t):
                result.append(t)
            else:
                result.append(words[word_idx])
                word_idx += 1
        return ''.join(result)
    else:
        return ''.join(reversed_tokens)

def is_bullet_line(line):
    stripped = line.lstrip()
    return stripped.startswith(("-", "*", "•", "▪", "‣"))

def normalize_bullet_line(line):
    # Remove any common bullet characters and leading whitespace
    cleaned = re.sub(r"^[-•*▪‣\s]+", "", line)
    return "- " + cleaned

def convert_pdf_to_txt(pdf_file_full_path, txt_file_full_path):
    with pdfplumber.open(pdf_file_full_path) as pdf:
        all_text = ""
        num_pages = len(pdf.pages)
        for index, page in enumerate(pdf.pages):
            print("Page {} of {}".format(index + 1, num_pages))
            page_text = page.extract_text()
            if page_text:
                all_text += f"Page {index + 1}\n"
                for line in page_text.splitlines():
                    fixed_line = fix_line_direction(line)
                    if is_bullet_line(line):
                        fixed_line = normalize_bullet_line(fixed_line)
                    all_text += fixed_line + "\n"
                all_text += "\n\n"  # Two line breaks after each page

    with open(txt_file_full_path, "w", encoding="utf-8") as f:
        f.write(all_text)






def main():
    current_folder_full_path = os.getcwd()
    parent_folder_full_path = os.path.dirname(current_folder_full_path)
    subfolder_name = 'advanced_emt'
    subfolder_full_path = os.path.join(parent_folder_full_path, subfolder_name)
    file_name = 'lesson_02_introduction_to_senior_cell'
    pdf_file_name = file_name + '.pdf'
    txt_file_name = file_name + '.txt'

    pdf_file_full_path = os.path.join(subfolder_full_path, pdf_file_name)
    txt_file_full_path = os.path.join(subfolder_full_path, txt_file_name)

    convert_pdf_to_txt(pdf_file_full_path, txt_file_full_path)


main()
