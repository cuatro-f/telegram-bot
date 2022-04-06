# инфа отсюда https://python-scripts.com/create-pdf-pyfpdf
from fpdf import FPDF


def add_image(image_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=10, y=8, w=180)
    pdf.set_font("Arial", size=12)
    pdf.ln(85)  # ниже на 85
    pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
    pdf.output("data/manga_pdf/add_image.pdf")


if __name__ == '__main__':
    add_image('data/manga/page-1.bmp')