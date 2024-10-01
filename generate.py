import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
import argparse


def create_paragraph(text, style, width):
    p = Paragraph(text, style)
    p.wrapOn(c, width, inch)
    return p


def draw_paragraph(p, x, y):
    p.drawOn(c, x, y - p.height)
    return y - p.height


def create_pdf_form(yaml_data, output_pdf):
    global c  # Make canvas global so it can be used in create_paragraph
    c = canvas.Canvas(output_pdf, pagesize=letter)
    form = c.acroForm
    width, height = letter
    margin = 50
    y = height - margin
    text_width = width - 2 * margin

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Heading2']

    # Add metadata
    p = create_paragraph(f"<b>{yaml_data.get('name', '')}</b>", title_style, text_width)
    y = draw_paragraph(p, margin, y) - 10

    p = create_paragraph(yaml_data.get('description', ''), normal_style, text_width)
    y = draw_paragraph(p, margin, y) - 20

    for task in yaml_data.get('tasks', []):
        question = task.get('question', '')
        urn = task.get('urn', '')

        # Draw URN
        p = create_paragraph(f"<b>{urn}</b>", normal_style, text_width)
        y = draw_paragraph(p, margin, y) - 5

        # Draw question
        p = create_paragraph(question, normal_style, text_width)
        y = draw_paragraph(p, margin, y) - 10

        # Create form fields
        form.textfield(name=f"{urn}_answer",
                       tooltip='Answer',
                       x=margin, y=y - 60,
                       width=text_width, height=50)
        y -= 70

        form.textfield(name=f"{urn}_remarks",
                       tooltip='Remarks',
                       x=margin, y=y - 40,
                       width=text_width, height=30)
        y -= 50

        # Add more fields as needed (timestamp, author, etc.)

        y -= 20  # Space between questions

        if y < 100:  # Start a new page if we're running out of space
            c.showPage()
            y = height - margin

    c.save()


def main():
    parser = argparse.ArgumentParser(description='Create PDF form from YAML')
    parser.add_argument('input_yaml', help='Path to the input YAML file')
    parser.add_argument('output_pdf', help='Path to save the output PDF form')
    args = parser.parse_args()

    # Read YAML file
    with open(args.input_yaml, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    # Create PDF form
    create_pdf_form(yaml_data, args.output_pdf)
    print(f"PDF form created and saved to {args.output_pdf}")


if __name__ == "__main__":
    main()