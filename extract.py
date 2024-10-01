import yaml
from PyPDF2 import PdfReader
import argparse


def extract_pdf_data(pdf_path):
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()

    # Create a nested dictionary structure
    data = {}
    for key, value in fields.items():
        if hasattr(value, 'value'):
            keys = key.split('_')
            current = data
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value.value

    return data


def save_yaml(data, output_path):
    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description='Extract PDF form data to YAML')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('output_yaml', help='Path to save the output YAML file')
    args = parser.parse_args()

    data = extract_pdf_data(args.input_pdf)
    save_yaml(data, args.output_yaml)
    print(f"Data extracted and saved to {args.output_yaml}")


if __name__ == "__main__":
    main()