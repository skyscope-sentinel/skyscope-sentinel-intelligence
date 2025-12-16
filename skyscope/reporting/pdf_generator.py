from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
import time
from .persona import Persona

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

    def generate(self, filename: str, query: str, simulation_content: str, intel_context: list):
        doc = SimpleDocTemplate(f"{self.output_dir}/{filename}", pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []

        # Title Page
        Story.append(Spacer(1, 100))
        Story.append(Paragraph("CLASSIFIED INTELLIGENCE TRAJECTORY REPORT", self.styles['ReportTitle']))
        Story.append(Spacer(1, 30))
        Story.append(Paragraph(f"SUBJECT: {query.upper()}", self.styles['Heading2']))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f"DATE: {time.strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        Story.append(Spacer(1, 50))
        
        # Persona Sign-off on Title
        Story.append(Paragraph(f"PREPARED BY: {Persona.NAME}", self.styles['Heading3']))
        Story.append(Paragraph(f"{Persona.TITLE}", self.styles['Normal']))
        Story.append(Paragraph(f"ABN: {Persona.ABN}", self.styles['Normal']))
        Story.append(PageBreak())

        # Intelligence Summary
        Story.append(Paragraph("1. Intelligence Summary", self.styles['Heading1']))
        Story.append(Paragraph(f"The following analysis leverages {len(intel_context)} verified intelligence vectors including Russian, Western, and Independent sources.", self.styles['Justify']))
        Story.append(Spacer(1, 12))
        for item in intel_context:
            source = item.get('source', 'Unknown')
            content = item.get('content', '')
            Story.append(Paragraph(f"<b>{source}:</b> {content}", self.styles['Justify']))
            Story.append(Spacer(1, 6))
        
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
