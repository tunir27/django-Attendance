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

from random import choice
from reportlab.lib.colors import HexColor
from time import gmtime, strftime
from datetime import date

def get_random_colors(no_colors):
    # generate random hexa
    colors_list = []
    for i in range(no_colors):
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colors_list.append(HexColor('#'+color))
    return colors_list

legendcolors = get_random_colors(10)


pdfmetrics.registerFont(TTFont('FreeSans', STATIC_ROOT + 'fonts/FreeSans.ttf'))
pdfmetrics.registerFont(
TTFont('FreeSansBold', STATIC_ROOT + 'fonts/FreeSansBold.ttf'))


from calendar import monthrange

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

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontName = 'FreeSansBold'
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100*mm, 15*mm, str(number))

    def legend_draw(self, labels, chart, **kwargs):
        legend = Legend()
        chart_type = kwargs['type']
        legend.fontName = 'FreeSans'
        legend.fontSize = 13
        legend.strokeColor = None
        if 'x' in kwargs:
            legend.x = kwargs['x']
        if 'y' in kwargs:
            legend.y = kwargs['y']
        legend.alignment = 'right'
        if 'boxAnchor' in kwargs:
            legend.boxAnchor = kwargs['boxAnchor']
        if 'columnMaximum' in kwargs:
            legend.columnMaximum = kwargs['columnMaximum']
        # x-distance between neighbouring swatche\s
        legend.deltax = 0
        lcolors = legendcolors
        if chart_type == 'pie':
            lcolors = [colors.green, colors.red]
        legend.colorNamePairs = list(zip(lcolors, labels))

        for i, color in enumerate(lcolors):
##            if chart_type == 'line':
##                chart.lines[i].fillColor = color
            if chart_type == 'pie':
                chart.slices[i].fillColor = color
##            elif chart_type == 'bar':
##                chart.bars[i].fillColor = color
        return legend
        


    def pie_chart_draw(self, values, llabels):
        d = Drawing(10, 150)
        # chart
        pc = Pie()
        pc.x = 0
        pc.y = 50
        # set data
        pc.data = values
        # set labels
        percentage = []
        for value in values:
            v = round(value, 2)
            percentage.append(str(v)+" %")
        pc.labels = percentage
        # set the link line between slice and it's label
        pc.sideLabels = 1
        # set width and color for slices
        pc.slices.strokeWidth = 0
        pc.slices.strokeColor = None
        d.add(self.title_draw(250, 180,
                              'Student Attendance Percentage'))
        d.add(pc)
        d.add(self.legend_draw(llabels, pc, x=300, y=150, boxAnchor='ne',
                               columnMaximum=12, type='pie'))
        return d
        

    def report(self, attendance_history,details,date,pie, title,pdf_type):
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
        styles.add(ParagraphStyle(
            name="Note", fontSize=11,alignment=TA_JUSTIFY, fontName="FreeSansBold"))
        # list used for elements added into document
        data = []
        data.append(Paragraph(title, styles['Title']))
        # insert a blank space
        data.append(Spacer(1, 12))
        table_data = []
        print("pdf_type",pdf_type)
        if pdf_type==1:
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
                data.append(Spacer(1, 6))
                # add a row to table
                try:
                    h,m,s=ah.duration.split(":")
                except:
                    h=0
                if not ah.in_time or not ah.out_time or int(h)<6:
                    table_data.append(
                    [
                     Paragraph(str(d.first_name)+" "+str(d.last_name)+"*", styles['Justify']),
                     Paragraph(str(ah.date), styles['Justify']),
                     Paragraph(str(ah.in_time), styles['Justify']),
                     Paragraph(str(ah.out_time), styles['Justify']),
                     Paragraph(str(ah.duration), styles['Justify']),
                     Paragraph(str(ah.status), styles['Justify']),])
                    
                else:
                    table_data.append(
                        [
                         Paragraph(str(d.first_name)+" "+str(d.last_name), styles['Justify']),
                         Paragraph(str(ah.date), styles['Justify']),
                         Paragraph(str(ah.in_time), styles['Justify']),
                         Paragraph(str(ah.out_time), styles['Justify']),
                         Paragraph(str(ah.duration), styles['Justify']),
                         Paragraph(str(ah.status), styles['Justify']),])
            # create table
            ah_table = Table(table_data, colWidths=[doc.width/5.8]*8)
            ah_table.hAlign = 'LEFT'
            ah_table.setStyle(TableStyle(
                [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                 ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                 ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                 ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
            data.append(ah_table)
            data.append(Spacer(1, 48))
        else:
            # table header
            dates=attendance_history.values('date').distinct()
            for i in range(len(dates)):
                table_data.append([
                    Paragraph('Student Name', styles['TableHeader']),
                    Paragraph('Date', styles['TableHeader']),
                    Paragraph('IN Time', styles['TableHeader']),
                    Paragraph('Out Time', styles['TableHeader']),
                    Paragraph('Duration', styles['TableHeader']),
                    Paragraph('Status', styles['TableHeader'])])
                # add a row to table
                for ah in attendance_history:
                    User = get_user_model()
                    uid=User.objects.filter(sid=ah.st_id)
                    d=Student_Details.objects.get(st_id=uid[0])
                    data.append(Spacer(1, 6))
                    if not ah.date==dates[i]['date']:
                        continue
                    else:
                        try:
                            h,m,s=ah.duration.split(":")
                        except:
                            h=0
                        if not ah.in_time or not ah.out_time or int(h)<6:
                            table_data.append(
                            [
                             Paragraph(str(d.first_name)+" "+str(d.last_name)+"*", styles['Justify']),
                             Paragraph(str(ah.date), styles['Justify']),
                             Paragraph(str(ah.in_time), styles['Justify']),
                             Paragraph(str(ah.out_time), styles['Justify']),
                             Paragraph(str(ah.duration), styles['Justify']),
                             Paragraph(str(ah.status), styles['Justify']),])
                            
                        else:
                            table_data.append(
                                [
                                 Paragraph(str(d.first_name)+" "+str(d.last_name), styles['Justify']),
                                 Paragraph(str(ah.date), styles['Justify']),
                                 Paragraph(str(ah.in_time), styles['Justify']),
                                 Paragraph(str(ah.out_time), styles['Justify']),
                                 Paragraph(str(ah.duration), styles['Justify']),
                                 Paragraph(str(ah.status), styles['Justify']),])
                # create table
                ah_table = Table(table_data, colWidths=[doc.width/5.8]*8)
                ah_table.hAlign = 'LEFT'
                ah_table.setStyle(TableStyle(
                    [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                     ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                     ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                     ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
                data.append(ah_table)
                data.append(Spacer(1, 48))
                table_data=[]
        # add pie chart
        if pie:
            d,m,y=date.split("/")
            s_date,t_days=monthrange(int(y),int(m))
            today = strftime("%d/%m/%y", gmtime())
            #present_per=(attendance_history.filter(out_time__isnull=False).exclude(date=today).count()/t_days)*100
            present_per=(attendance_history.filter(status="1").exclude(date=today).count()/t_days)*100
            absent_per=100-present_per
            att_percentage=[present_per,absent_per]
            llabels = ['Present','Absent']
            pie_chart = self.pie_chart_draw(att_percentage, llabels)
            data.append(pie_chart)
        # create document
        data.append(Paragraph("* denotes DEFAULTERS.",styles['Note']))
        data.append(Paragraph("0 denotes ABSENT and 1 denotes PRESENT.",styles['Note']))
        doc.build(data, onFirstPage=self.pageNumber,
                  onLaterPages=self.pageNumber)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
