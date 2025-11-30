from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(target, scan_output, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "PortXplore - Scan Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 725, f"Target: {target}")

    text = c.beginText(50, 700)
    text.setFont("Helvetica", 10)

    for line in scan_output.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()
