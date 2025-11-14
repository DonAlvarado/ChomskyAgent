from __future__ import annotations
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
import uuid
from graphviz import Source

from Back.utils.file_manager import ensure_dir
from Back.utils.logger import get_logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "Front", "static", "generated")
OUTPUT_DIR = os.path.normpath(OUTPUT_DIR)

log = get_logger("PDFReporter")


class PDFReporter:

    def __init__(self):
        ensure_dir(OUTPUT_DIR)

    def _save_diagram(self, dot: str) -> str:
        g = Source(dot)
        img_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.png")
        g.render(img_path, format="png", cleanup=True)
        full_path = img_path + ".png"
        log.info(f"Diagrama guardado en {full_path}")
        return full_path

    def generate_pdf(self, title: str, info: dict, dot: str = None) -> str:
        file_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(40, 750, title)

        y = 720
        c.setFont("Helvetica", 12)

        for key, val in info.items():
            line = f"{key}: {val}"
            c.drawString(40, y, line)
            y -= 18
            if y < 80:
                c.showPage()
                y = 750

        if dot:
            img = self._save_diagram(dot)
            if y < 250:
                c.showPage()
                y = 750
            c.drawImage(ImageReader(img), 40, y - 240, width=400, height=240)

        c.save()
        log.info(f"PDF generado en {file_path}")
        return file_path
