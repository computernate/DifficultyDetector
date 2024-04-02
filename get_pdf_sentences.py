import PyPDF2
import re

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(28, 40):  # Adjust page numbers as needed (0-indexed)
            page = reader.pages[page_num]
            yield page.extract_text()


def get_sections(text):
    sections = {}
    current_section = None
    previous_line = ""
    for line in text.split('\n'):
        # Check if the line is a section header
        if re.match(r'\d+\.\d+\.\d+.*', line):
            current_section = line.strip()
            sections[current_section] = []
        elif current_section:
            # Exclude page numbers and standalone headers
            if not re.match(r'\d+$', line) and not re.match(r'\d+\.\d+.*', line) and not line.startswith('CHAPTER'):
                sections[current_section].append(line.strip())
        previous_line = line
    return sections


def main():
    pdf_path = 'D:/nater/Documents/DifficultyDetector/Japanese Grammar Guide.pdf'
    all_text = ''
    for page_text in extract_text_by_page(pdf_path):
        all_text += page_text + '\n'

    sections = get_sections(all_text)
    for section, content in sections.items():
        print(f'{section}:')
        print('\n'.join(content))
        print('---')

if __name__ == '__main__':
    main()