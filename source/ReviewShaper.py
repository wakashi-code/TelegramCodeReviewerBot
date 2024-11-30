from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from source.File import File

class ReviewShaper:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Times-New-Roman', r'C:\Windows\Fonts\times.ttf'))

    def generate_zip_review(self, file: File, data: str):
        reviews = []
        for _file in file.neasted:
            reviews.append(self.generate_review(_file, data))
        return reviews

    def generate_review(self, file: File, data: str):
        file_name = f"{file.name} - Review.pdf"
        lines = data.splitlines()
        y = PAGE_HEIGHT - 40

        canvs = canvas.Canvas(f"{file.name} - Review.pdf", pagesize=letter)
        canvs.setFont("Times-New-Roman", 12)

        for line in lines:
            if y - LINE_HEIGHT < 40:
                canvs.showPage()
                canvs.setFont("Times-New-Roman", 12)
                y = PAGE_HEIGHT - 40

            max_length = 85
            current_posistion = 0;
            while current_posistion < len(line):
                end_position = current_posistion + max_length
                canvs.drawString(40, y, line[current_posistion:end_position])
                current_posistion += max_length
                y -= LINE_HEIGHT
        canvs.save();

        return file_name

PAGE_WIDTH, PAGE_HEIGHT = letter
LINE_HEIGHT = 12