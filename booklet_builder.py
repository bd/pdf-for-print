#!/usr/bin/env python3
"""
Reorder PDF pages for booklet (signature) printing with imposition overlays.

For an 8‐page signature the desired mapping is:
  Source P1 → S1FR  (I2)
  Source P2 → S1BL  (I3)
  Source P3 → S2FR  (I6)
  Source P4 → S2BL  (I7)
  Source P5 → S2BR  (I8)
  Source P6 → S2FL  (I5)
  Source P7 → S1BR  (I4)
  Source P8 → S1FL  (I1)

That is, the imposed output order (for 8 pages) is:
  I1: S1FL ← Source P8
  I2: S1FR ← Source P1
  I3: S1BR ← Source P7
  I4: S1BL ← Source P2
  I5: S2FL ← Source P6
  I6: S2FR ← Source P3
  I7: S2BR ← Source P5
  I8: S2BL ← Source P4

Generalized for a signature of N pages (N a multiple of 4), for each sheet i (0‑indexed, with sheet label S{i+1}) define:
    • Front Left (FL)  = sig_pages[N – 1 – 2*i]
    • Front Right (FR) = sig_pages[2*i]
    • Back Right (BR)  = sig_pages[N – 2 – 2*i]
    • Back Left (BL)   = sig_pages[2*i + 1]
Output the pages in that order: [FL, FR, BR, BL].

An overlay showing the imposition label and global output page number (I<n>) is applied
only if the overlay option is enabled.
By default the back pages are rotated 180°.
Default signature size is 20 pages.

Dependencies: PyPDF2==3.0.1, reportlab==4.3.0
"""

import argparse
import sys
import io
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas

class BookletReorder:
    def __init__(self, input_pdf_path: str):
        self.reader = PdfReader(input_pdf_path)
        self.pages = list(self.reader.pages)
        if not self.pages:
            raise ValueError("Input PDF contains no pages.")
        self.pages_per_signature = 4  # will be overridden by command-line default
        self.rotate_back = True       # default: rotate back pages
        self.overlay = False          # default: no imposition overlay
        self.overlay_position = (20, 20)

    def set_pages_per_signature(self, count: int):
        if count % 4 != 0:
            raise ValueError("Pages per signature must be a multiple of 4.")
        self.pages_per_signature = count
        return self

    def set_rotate_back(self, rotate: bool):
        self.rotate_back = rotate
        return self

    def enable_overlay(self, enabled: bool):
        self.overlay = enabled
        return self

    def _create_blank_page(self) -> PageObject:
        mb = self.pages[0].mediabox
        return PageObject.create_blank_page(width=mb.width, height=mb.height)

    def _pad_signature(self, sig_pages: list) -> list:
        remainder = len(sig_pages) % 4
        if remainder:
            for _ in range(4 - remainder):
                sig_pages.append(self._create_blank_page())
        return sig_pages

    def _create_overlay(self, text: str, page: PageObject) -> PageObject:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.setFont("Helvetica", 10)
        c.drawString(self.overlay_position[0], self.overlay_position[1], text)
        c.save()
        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        return overlay_pdf.pages[0]

    def _impose_signature(self, sig_pages: list, sig_global_start: int) -> list:
        sig_pages = self._pad_signature(sig_pages)
        N = len(sig_pages)
        sheets = N // 4
        imposed = []
        global_page = sig_global_start
        for i in range(sheets):
            FL = sig_pages[N - 1 - 2 * i]       # Front Left
            FR = sig_pages[2 * i]               # Front Right
            BR = sig_pages[N - 2 - 2 * i]         # Back Right
            BL = sig_pages[2 * i + 1]             # Back Left
            sheet_order = [FL, FR, BR, BL]
            suffixes = ["FL", "FR", "BR", "BL"]
            for pos, page in enumerate(sheet_order):
                label = f"S{i+1}{suffixes[pos]} (I{global_page})"
                if self.overlay:
                    overlay = self._create_overlay(label, page)
                    page.merge_page(overlay)
                if self.rotate_back and suffixes[pos] in ("BR", "BL"):
                    page.rotate(180)
                imposed.append(page)
                global_page += 1
        return imposed

    def build(self, output_pdf_path: str):
        writer = PdfWriter()
        total = len(self.pages)
        sig_size = self.pages_per_signature
        imposed_pages = []
        global_counter = 1
        for start in range(0, total, sig_size):
            sig = self.pages[start:start + sig_size]
            imposed = self._impose_signature(sig, global_counter)
            imposed_pages.extend(imposed)
            global_counter += len(imposed)
        for page in imposed_pages:
            writer.add_page(page)
        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)

def main():
    parser = argparse.ArgumentParser(
        description="Reorder PDF pages for booklet printing with imposition overlays."
    )
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", help="Output imposed PDF file")
    parser.add_argument(
        "--pages-per-signature",
        type=int,
        default=20,
        help="Number of pages per signature (multiple of 4). Default is 20."
    )
    parser.add_argument(
        "--no-rotate-back",
        action="store_true",
        help="Do not rotate back pages (default rotates back pages)."
    )
    parser.add_argument(
        "--overlay",
        action="store_true",
        help="Enable imposition overlay (default is off)."
    )
    args = parser.parse_args()

    try:
        br = BookletReorder(args.input)
        br.set_pages_per_signature(args.pages_per_signature)\
          .set_rotate_back(not args.no_rotate_back)\
          .enable_overlay(args.overlay)
        br.build(args.output)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()