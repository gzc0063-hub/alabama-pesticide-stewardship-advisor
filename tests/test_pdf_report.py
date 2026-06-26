from src.pdf_report import build_text_pdf


def test_build_text_pdf_creates_pdf_bytes():
    pdf = build_text_pdf("# Report\n\n- County: Lee County")

    assert pdf.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf
