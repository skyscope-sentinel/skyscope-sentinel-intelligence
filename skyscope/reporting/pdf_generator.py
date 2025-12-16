import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from .persona import Persona
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

class PDFReportGenerator:
    def __init__(self, output_dir="."):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        self.styles.add(ParagraphStyle(
            name='Justify',
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            fontSize=10,
            leading=12
        ))
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=24,
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='FooterData',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontSize=8,
            textColor=colors.gray
        ))

        
        Story.append(PageBreak())

        # Strategic Simulation
        Story.append(Paragraph("2. Strategic Simulation & Trajectory", self.styles['Heading1']))
        # Split content by newlines to handle basic formatting of LLM output
        for line in simulation_content.split('\n'):
            if line.strip():
                if line.startswith('#'):
                     Story.append(Paragraph(line.strip('# '), self.styles['Heading2']))
                else:
                    Story.append(Paragraph(line, self.styles['Justify']))
                Story.append(Spacer(1, 6))

        # Build
        doc.build(Story)
        return f"{self.output_dir}/{filename}"
