import pdfplumber
import re
import os

def is_hebrew(char):
    return '\u0590' <= char <= '\u05FF'

def is_hebrew_word(word):
    return any(is_hebrew(c) for c in word)

def fix_line_direction(line):
    tokens = re.split(r'(\s+)', line)  # split by whitespace but keep separators
    reversed_tokens = [token[::-1] if is_hebrew_word(token) else token for token in tokens]

    # Count how many non-space tokens are Hebrew
    word_tokens = [t for t in reversed_tokens if not re.match(r'\s+', t)]
    hebrew_word_count = sum(1 for t in word_tokens if is_hebrew_word(t))

    if len(word_tokens) > 0 and hebrew_word_count >= len(word_tokens) / 2:
        # Line is mostly Hebrew: reverse word order (preserving whitespace)
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

def convert_pdf_to_txt(pdf_file_full_path, txt_file_full_path):
    with pdfplumber.open(pdf_file_full_path) as pdf:
        all_text = ""
        num_pages = len(pdf.pages)
        for index, page in enumerate(pdf.pages):
            print("Page {} of {}".format(index + 1, num_pages))
            page_text = page.extract_text()
            if page_text:
                fixed_lines = [fix_line_direction(line) for line in page_text.splitlines()]
                all_text += f"Page {index + 1}\n"  # Add page number as a separate line
                all_text += '\n'.join(fixed_lines)
                all_text += '\n\n'  # Two line breaks at the end of the page

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
