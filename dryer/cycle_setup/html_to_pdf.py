"""."""

from weasyprint import HTML

html = HTML("index.html")
html.write_pdf("report.pdf")
