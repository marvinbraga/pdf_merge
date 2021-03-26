# encoding-utf8
"""
Marcus Vinicius Braga, 2021.
Pdf to Image to Pdf.
"""

from wand.image import Image as wi
from pikepdf import Pdf, PdfImage

pdf = wi(filename='insumos/merged.pdf')
images = pdf.convert('png')

doc = Pdf.new()
for img in images.sequence:
    pdf_image = PdfImage(img)
    doc.pages.extend(pdf_image)

doc.save('output/from_image.pdf')
