import pdfplumber


def detect_bank(file_path: str):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]
        if page:
            footer = page.crop(
                bbox=(0, page.height / 2, page.width, page.height)
            ).extract_text()

            if "C.I.H siège social" in footer:
                return "cih"

            if "Attijariwafa bank société anonyme" in footer:
                return "awb"
