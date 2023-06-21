from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, ListStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageTemplate, Frame, Table, TableStyle, ListFlowable, ListItem
from reportlab.platypus.flowables import HRFlowable, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# Define custom styles for PDF generation
pdf_title_style = ParagraphStyle(
    "title",
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=30,
    textColor="#333333",
)
pdf_section_style = ParagraphStyle(
    "section",
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=24,
    textColor="#333333",
    spaceBefore=5 * mm,
    spaceAfter=2.5 * mm,
)
pdf_text_style = ParagraphStyle(
    "text",
    fontName="Helvetica",
    fontSize=12,
    leading=18,
    textColor="#666666",
    spaceBefore=2.5 * mm,
    spaceAfter=2.5 * mm,
    alignment=TA_JUSTIFY,
)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm, f"Page {self._pageNumber} of {page_count}")

def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    page_num_total = doc.page
    text = f"Page {page_num} of {page_num_total}"
    canvas.drawRightString(200*mm, 20*mm, text)
    # canvas.drawCentredString(100*mm, 20*mm, "Document controlled only when viewed on the SciSpaceLIMS")
    

def df2table(df):
    return Table([[Paragraph(col) for col in df.columns]] + df.values.tolist(),
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
      hAlign = 'LEFT')

def dict2table(d):
    return Table([[Paragraph(k), Paragraph(v)] for k, v in d.items()],
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
      hAlign = 'LEFT')