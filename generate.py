import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
import argparse

def create_pdf_form(yaml_data, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    form = c.acroForm

    y = 750  # Starting y position

    def add_fields(data, prefix=''):
        nonlocal y
        for key, value in data.items():
            full_key = f"{prefix}{key}"
            if isinstance(value, dict):
                c.drawString(50, y, full_key.capitalize() + ':')
                y -= 20
                add_fields(value, prefix=f"{full_key}_")
            else:
                c.drawString(100, y, key.replace('_', ' ').capitalize())
                form.textfield(name=full_key,
                               tooltip=full_key,
                               x=250, y=y-15,
                               width=300, height=20)
                y -= 30
        y -= 10  # Extra space between sections

    add_fields(yaml_data)
    c.save()

def main():
    parser = argparse.ArgumentParser(description='Create PDF form from YAML')
    parser.add_argument('input_yaml', help='Path to the input YAML file')
    parser.add_argument('output_pdf', help='Path to save the output PDF form')
    args = parser.parse_args()

    # Read YAML file
    with open(args.input_yaml, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Create PDF form
    create_pdf_form(yaml_data, args.output_pdf)
    print(f"PDF form created and saved to {args.output_pdf}")

if __name__ == "__main__":
    main()