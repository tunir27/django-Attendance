from django.utils.translation import ugettext_lazy as _
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle

from Project.settings import STATIC_ROOT
from .models import Student_Attendance,Student_Details
from django.contrib.auth import get_user_model

pdfmetrics.registerFont(TTFont('FreeSans', STATIC_ROOT + 'fonts/FreeSans.ttf'))
pdfmetrics.registerFont(
TTFont('FreeSansBold', STATIC_ROOT + 'fonts/FreeSansBold.ttf'))

class PdfPrint:

    # initialize class
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100*mm, 15*mm, str(number))

    def report(self, attendance_history,details, title):
        # set some characteristics for pdf document
        doc = SimpleDocTemplate(
            self.buffer,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72,
            pagesize=self.pageSize)

        # a collection of styles offer by the library
        styles = getSampleStyleSheet()
        # add custom paragraph style
        styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY, fontName="FreeSans"))
        # list used for elements added into document
        data = []
        data.append(Paragraph(title, styles['Title']))
        # insert a blank space
        data.append(Spacer(1, 12))
        table_data = []
        # table header
        table_data.append([
            Paragraph('Student Name', styles['TableHeader']),
            Paragraph('Date', styles['TableHeader']),
            Paragraph('IN Time', styles['TableHeader']),
            Paragraph('Out Time', styles['TableHeader']),
            Paragraph('Duration', styles['TableHeader']),
            Paragraph('Status', styles['TableHeader'])])
        for ah in attendance_history:
            User = get_user_model()
            uid=User.objects.filter(sid=ah.st_id)
            d=Student_Details.objects.get(st_id=uid[0])
            print(d)
            data.append(Spacer(1, 6))
            # add a row to table
            table_data.append(
                [
                 Paragraph(str(d.first_name)+" "+str(d.last_name), styles['Justify']),
                 Paragraph(str(ah.date), styles['Justify']),
                 Paragraph(str(ah.in_time), styles['Justify']),
                 Paragraph(str(ah.out_time), styles['Justify']),
                 Paragraph(str(ah.duration), styles['Justify']),
                 Paragraph(str(ah.status), styles['Justify']),])
        # create table
        ah_table = Table(table_data, colWidths=[doc.width/6.0]*6)
        ah_table.hAlign = 'LEFT'
        ah_table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        data.append(ah_table)
        data.append(Spacer(1, 48))
        # create document
        doc.build(data, onFirstPage=self.pageNumber,
                  onLaterPages=self.pageNumber)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
