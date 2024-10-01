import yaml
from PyPDF2 import PdfReader
import argparse
from datetime import datetime
import os
import subprocess
from PyPDF2.generic import TextStringObject


def get_git_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except:
        return "Unknown"


def extract_value(obj):
    if isinstance(obj, TextStringObject):
        return str(obj)
    elif isinstance(obj, dict) and '/V' in obj:
        return extract_value(obj['/V'])
    return str(obj)


def extract_pdf_data(pdf_path):
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()

    # Extract metadata from the first page
    first_page = reader.pages[0]
    text = first_page.extract_text()
    name = text.split('\n')[0]  # Assuming the name is the first line

    # Create the basic structure
    data = {
        "provenance": {
            "git_commit_hash": get_git_hash(),
            "timestamp": datetime.now().isoformat(),
            "uri": os.path.abspath(pdf_path),
            "author": "Unknown"  # You might want to add a way to input this
        },
        "name": name,
        "urn": "Unknown",  # You might want to add a way to input this
        "date": datetime.now().strftime("%Y-%m-%d"),
        "contents": []
    }

    # Process form fields
    for key, value in fields.items():
        if key.endswith('_answer'):
            urn = key[:-7]  # Remove '_answer' from the end
            question_text = next((q for q in text.split('\n') if urn in q), '')
            answer_text = extract_value(value)
            remarks_text = extract_value(fields.get(f"{urn}_remarks", {}))

            content = {
                "question": question_text,
                "urn": urn,
                "answer": answer_text,
                "remarks": remarks_text,
                "authors": [{"name": "Unknown"}],  # You might want to add a way to input this
                "timestamp": datetime.now().isoformat()
            }
            data["contents"].append(content)

    return data


def save_yaml(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def main():
    parser = argparse.ArgumentParser(description='Extract PDF form data to structured YAML')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('output_yaml', help='Path to save the output YAML file')
    args = parser.parse_args()

    data = extract_pdf_data(args.input_pdf)
    save_yaml(data, args.output_yaml)
    print(f"Data extracted and saved to {args.output_yaml}")


if __name__ == "__main__":
    main()