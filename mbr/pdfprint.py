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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from datetime import datetime

import base64
import io

from django.utils import timezone

from uamc.settings import BASE_DIR

legendcolors = '#576563'

pdfmetrics.registerFont(TTFont('RobotoLight', BASE_DIR + '/mbr/static/mbr/fonts/RobotoLight/RobotoLight.ttf'))
pdfmetrics.registerFont(TTFont('RobotoBold', BASE_DIR + '/mbr/static/mbr/fonts/RobotoBold/RobotoBold.ttf'))

pdfmetrics.registerFont(TTFont('UbuntuMedium', BASE_DIR + '/mbr/static/mbr/fonts/UbuntuFonts/Ubuntu-M.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuLight', BASE_DIR + '/mbr/static/mbr/fonts/UbuntuFonts/Ubuntu-L.ttf'))

class RotadedImage(Image):
    def wrap(self, availWidth, availHeight):
        h, w = Image.wrap(self, availHeight, availWidth)
        return w, h

    def draw(self):
        self.canv.rotate(90)
        self.canv.translate(-1 *mm, -176 * mm)
        Image.draw(self)


class PdfPrint:
    def __init__(self, buffer, filename, context, pageSize):
        self.buffer = buffer
        self.filename = filename
        self.context = context
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize
        self.sitename = 'http://127.0.0.1:8080'

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()

        dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S %Z')
        year = datetime.utcnow().strftime('%Y')
        canvas.setFont('UbuntuLight', 7)
        canvas.drawCentredString(100 * mm, 10 * mm, 'Page '+str(number))
        canvas.drawCentredString(37 * mm, 10 * mm, 'MeteoBriefing © UAMC  ' + year)
        canvas.drawCentredString(177 * mm, 10 * mm, 'Printed: '+dt +'UTC')
        canvas.setFont('UbuntuLight', 9)
        canvas.setLineWidth(mm * 0.01)
        canvas.line(20 * mm, 13 * mm, 196 * mm, 13 * mm)

        company = 'Provided by Ukrainian Aeronautical Meteorological Center'
        canvas.drawCentredString (105 * mm, 285 * mm, company)
        canvas.setFont('UbuntuLight', 7)
        contact = 'Met Office: +38(044)281-74743,+38(044)281-73341; Technical Support: +38(050)356-29555; +38(044)221-1434;'
        canvas.drawCentredString(110 * mm, 281 * mm, contact)
        canvas.line(20 * mm, 280 * mm, 196 * mm, 280 * mm)
        canvas.setLineWidth(0.5)

    def insertHeadlines(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100 * mm, 15 * mm, str(number))

    def drawImage(self, link):
        pass

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontName = 'RobotoBold'
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def header_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontName = 'RobotoBold'
        chart_title.fontSize = 9
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def legend_draw(self, labels, chart, **kwargs):
        legend = Legend()
        chart_type = kwargs['type']
        legend.fontName = 'RobotoBold'
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
        legend.deltax = 0
        lcolors = legendcolors
        if chart_type == 'line':
            lcolors = [colors.red, colors.blue]
        legend.colorNamePairs = zip(lcolors, labels)

        for i, color in enumerate(lcolors):
            if chart_type == 'line':
                chart.lines[i].fillColor = color
            elif chart_type == 'pie':
                chart.slices[i].fillColor = color
            elif chart_type == 'bar':
                chart.bars[i].fillColor = color
        return legend

    def line_chart_draw(self, values, days):
        nr_days = len(days)
        min_temp = min(min(values[0]), min(values[1]))
        d = Drawing(0, 170)
        chart = SampleHorizontalLineChart()
        chart.width = 350
        chart.height = 135
        chart.data = values
        chart.joinedLines = True
        chart.lineLabels.fontName = 'RobotoBold'
        chart.strokeColor = colors.white
        chart.fillColor = colors.lightblue
        chart.lines[0].strokeColor = colors.red
        chart.lines[0].strokeWidth = 2
        chart.lines[1].strokeColor = colors.blue
        chart.lines[1].strokeWidth = 2
        chart.lines.symbol = makeMarker('Square')
        chart.lineLabelFormat = '%2.0f'
        chart.categoryAxis.joinAxisMode = 'bottom'
        chart.categoryAxis.labels.fontName = 'RobotoBold'
        if nr_days > 7:
            chart.categoryAxis.labels.angle = 45
            chart.categoryAxis.labels.boxAnchor = 'e'
        chart.categoryAxis.categoryNames = days
        chart.valueAxis.labelTextFormat = '%2.0f °C'
        chart.valueAxis.valueStep = 10
        if min_temp > 0:
            chart.valueAxis.valueMin = 0
        llabels = ['Max temp', 'Min temp']
        d.add(self.title_draw(250, 180, _('Temperatures statistics')))
        d.add(chart)
        d.add(self.legend_draw(llabels, chart, x=400, y=150, type='line'))
        return d

    def pie_chart_draw(self, values, llabels):
        d = Drawing(10, 150)
        pc = Pie()
        pc.x = 0
        pc.y = 50
        pc.data = values
        pc.labels = get_percentage(values)
        pc.sideLabels = 1
        pc.slices.strokeWidth = 0
        pc.slices.strokeColor = None
        d.add(self.title_draw(250, 180,
                              _('Precipitation probability statistics')))
        d.add(pc)
        d.add(self.legend_draw(llabels, pc, x=300, y=150, boxAnchor='ne',
                               columnMaximum=12, type='pie'))
        return d

    def vertical_bar_chart_draw(self, values, days, llabels):
        d = Drawing(0, 170)
        bc = VerticalBarChart()
        bc.height = 125
        bc.width = 470
        bc.data = values
        bc.barSpacing = 0.5

        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.categoryNames = days

        bc.barLabelFormat = '%d'
        bc.barLabels.nudge = 7

        bc.valueAxis.labelTextFormat = '%d km/h'
        bc.valueAxis.valueMin = 0

        d.add(self.title_draw(250, 190, _('Wind speed statistics')))
        d.add(bc)
        d.add(self.legend_draw(llabels, bc, x=480, y=165, boxAnchor='ne',
                               columnMaximum=1, type='bar'))
        return d

    def mrl_chart_draw(self, title, type):
        pass

    def report(self, title):
        doc = SimpleDocTemplate(
            self.buffer,
            # self.filename,
            rightMargin=35,
            leftMargin=50,
            topMargin=45,
            bottomMargin=31,
            title=self.filename,
            author='MBR author',
            creator='MBR report system creator',
            pagesize=self.pageSize)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TableHeader', fontSize=11, alignment=TA_CENTER, fontName='RobotoBold'))
        styles.add(ParagraphStyle(name='ParagraphTitle', fontSize=11, alignment=TA_JUSTIFY, fontName='RobotoBold'))
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='RobotoBold'))
        styles.add(ParagraphStyle(name='PageHeader', fontSize=9, alignment=TA_CENTER, fontName='UbuntuLight'))
        styles.add(ParagraphStyle(name='PageHeaderContact', fontSize=7, alignment=TA_CENTER, fontName='UbuntuLight'))
        styles.add(ParagraphStyle(name='PageTitle', fontSize=14, alignment=TA_CENTER, fontName='UbuntuMedium'))
        styles.add(ParagraphStyle(name='PageFlightRoute', fontSize=11, alignment=TA_CENTER, fontName='UbuntuMedium'))
        styles.add(ParagraphStyle(name='TypeInfoTitle', fontSize=13, alignment=TA_CENTER, fontName='UbuntuMedium'))
        styles.add(ParagraphStyle(name='Index', fontSize=13, alignment=TA_JUSTIFY, fontName='UbuntuMedium'))
        styles.add(ParagraphStyle(name='IndexCenter', fontSize=13, alignment=TA_CENTER, fontName='UbuntuMedium'))
        styles.add(ParagraphStyle(name='Message', fontSize=12, leading = 15, fontName='UbuntuLight'))

        data = []
        data.append(Spacer(1, 12))
        title = 'FLIGHT DOCUMENTATION'
        data.append(Paragraph(title, styles['PageTitle']))
        data.append(Spacer(1, 12))
        airport_from = self.context['request_data']['airport_from']
        airport_to = self.context['request_data']['airport_to']
        flight = 'Flight #: ' +self.context['request_data']['number']
        spaces = '&nbsp;'*110
        route = 'Route: ' + airport_from +'-' +airport_to
        data.append(Paragraph(flight + spaces + route, styles['PageFlightRoute']))
        data.append(Spacer(1, 12))

        #Observation and forecasts
        subtitle = 'Airport reports and forecasts, en-route warnings'
        data.append(Paragraph(subtitle, styles['TypeInfoTitle']))
        data.append(Spacer(1, 12))
        for k, v in self.context['observation'].items():
            data.append(Paragraph(k, styles['Index']))
            data.append(Spacer(1, 5))
            data.append(Paragraph(v['message'], styles['Message']))
            forecast = self.context['forecast'][k]['message']
            data.append(Spacer(1, 5))
            data.append(Paragraph(forecast, styles['Message']))
            data.append(Spacer(1, 5))
        data.append(PageBreak())

        # SIGMETs
        data.append(Spacer(1, 12))
        subtitle = 'SIGMET'
        data.append(Paragraph(subtitle, styles['TypeInfoTitle']))
        for k, v in self.context['sigmets'].items():
            data.append(Paragraph(k, styles['Index']))
            for sigmet in self.context['sigmets'][k]:
                data.append(Paragraph(sigmet['message'], styles['Message']))
        data.append(PageBreak())

        # AIRMETs
        if 'airmets' in self.context:
            data.append(Spacer(1, 12))
            subtitle = 'AIRMET'
            data.append(Paragraph(subtitle, styles['TypeInfoTitle']))
            for k, v in self.context['airmets'].items():
                data.append(Paragraph(k, styles['Index']))
                for airmet in self.context['airmets'][k]:
                    data.append(Paragraph(airmet['message'], styles['Message']))
            data.append(PageBreak())

        # GAMETS
        if 'gamets' in self.context:
            data.append(Spacer(1, 12))
            subtitle = 'GAMET'
            data.append(Paragraph(subtitle, styles['TypeInfoTitle']))
            for k, v in self.context['gamets'].items():
                data.append(Paragraph(k, styles['Index']))
                for gamet in self.context['gamets'][k]:
                    data.append(Paragraph(gamet['message'], styles['Message']))
            data.append(PageBreak())

       # Volcanic
        '''if self.context['gamets']:
            for k, v in self.context['gamets'].items():
                data.append(Paragraph(k, styles['Index']))
                for message in self.context['gamets'][k]:
                    data.append(Paragraph(message['message'], styles['Message']))
        '''
        for key, value in self.context.items():
            if key == 'wafc_charts':
                for date_time, regions in value.items():
                    for region, flightlevels in regions.items():
                        for flightlevel, datamap in flightlevels.items():
                            map_image = base64.b64decode(datamap['base64'])
                            buffer_map = io.BytesIO(map_image)
                            if (flightlevel =='SM' ) or (flightlevel =='SH'):
                                titlemap = 'WAFC forecast of SIGWX (SWM) for region' + str(region)
                            else:
                                titlemap = 'WAFC forecast of upper wind and upper-air temperature for FL' + str(flightlevel)
                            data.append(Paragraph(titlemap, styles['TypeInfoTitle']))
                            data.append(Paragraph('valid '+ str(date_time), styles['TypeInfoTitle']))
                            image = RotadedImage(buffer_map, width=255 * mm, height=176 * mm, mask="auto")
                            data.append(image)
        data.append(PageBreak())

        #Radar meteorological phenomena chart
        map_image = base64.b64decode(self.context['phenomena_chart'][1])
        buffer_map = io.BytesIO(map_image)
        titlemap = 'Radar meteorological phenomena chart'
        data.append(Paragraph(titlemap, styles['TypeInfoTitle']))
        data.append(Spacer(1, 12))
        image =Image(buffer_map, width=435, height=335, mask="auto")
        data.append(Spacer(1, 12))
        data.append(image)
        data.append(Spacer(1, 12))

        #Radar echo heights chart
        map_image = base64.b64decode(self.context['heights_chart'][1])
        buffer_map = io.BytesIO(map_image)
        titlemap = 'Radar echo heights chart'
        data.append(Paragraph(titlemap, styles['TypeInfoTitle']))
        data.append(Spacer(1, 12))
        image = Image(buffer_map, width=435, height=335, mask="auto")
        data.append(image)

        # create document
        doc.build(data, onFirstPage=self.pageNumber, onLaterPages=self.pageNumber)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
