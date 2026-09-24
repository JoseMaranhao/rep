from __future__ import annotations

import shutil
from xml.sax.saxutils import escape
from datetime import datetime, timezone
from pathlib import Path

from .models import Finding, Photo, Report


def _copy_evidence(output: Path, evidence: list[Photo]) -> Path:
    evidence_dir = output / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    for photo in evidence:
        target = evidence_dir / photo.evidence_filename
        if not target.exists():
            shutil.copy2(photo.path, target)
    return evidence_dir


def build_report(title: str, findings: list[Finding], reviewed_photos: int, output: Path, evidence: list[Photo]) -> Path:
    """Write a PDF report and a sidecar directory of byte-for-byte evidence copies."""
    # Kept inside the function so evidence-only source operations work until PDF output is requested.
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    output.mkdir(parents=True, exist_ok=True)
    evidence_dir = _copy_evidence(output, evidence)
    report = Report(title=title, created_at=datetime.now(timezone.utc).isoformat(), findings=findings, reviewed_photos=reviewed_photos)
    target = output / "report.pdf"
    document = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=1.4 * cm, leftMargin=1.4 * cm, topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=12))
    warning = ParagraphStyle(name="Warning", parent=styles["BodyText"], backColor=colors.HexColor("#fff4ce"), borderColor=colors.HexColor("#c79300"), borderWidth=1, borderPadding=8, spaceAfter=12)
    story = [
        Paragraph(escape(report.title), styles["ReportTitle"]),
        Paragraph(f"Generated: {report.created_at}<br/>Photos reviewed: {report.reviewed_photos}<br/>Potential conditions listed: {len(report.findings)}", styles["BodyText"]),
        Spacer(1, 10),
        Paragraph("<b>Important:</b> This is an evidence-organizing aid, not a professional inspection or legal determination. Verify every item against the original photo. Keep the original photos and their metadata unchanged, and retain proof that you sent the verified report to your landlord.", warning),
        Paragraph("Findings", styles["Heading2"]),
    ]
    if report.findings:
        data = [[Paragraph("Category", styles["BodyText"]), Paragraph("Severity", styles["BodyText"]), Paragraph("Observation and location", styles["BodyText"]), Paragraph("Evidence file", styles["BodyText"])]]
        for finding in report.findings:
            data.append([
                Paragraph(escape(finding.category), styles["BodyText"]),
                Paragraph(escape(finding.severity), styles["BodyText"]),
                Paragraph(f"{escape(finding.description)}<br/><i>Location: {escape(finding.location)}; confidence: {escape(finding.confidence)}</i>", styles["BodyText"]),
                Paragraph(escape(finding.evidence_filename), styles["BodyText"]),
            ])
        table = Table(data, colWidths=[2.6 * cm, 2.1 * cm, 8.4 * cm, 4.1 * cm], repeatRows=1)
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f5")), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#aab7c2")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story.extend([table, Spacer(1, 12)])
    else:
        story.extend([Paragraph("No conditions were automatically listed. Review the photo appendix manually before sending this report.", styles["BodyText"]), Spacer(1, 12)])
    story.extend([PageBreak(), Paragraph("Photo appendix", styles["Heading2"]), Paragraph("The images below are working copies. The evidence directory next to this PDF contains the original downloaded/local files used to create the report.", styles["BodyText"]), Spacer(1, 8)])
    for index, photo in enumerate(evidence, start=1):
        caption = Paragraph(f"{index}. {escape(photo.evidence_filename)}<br/><font size=8>{escape(photo.source)}</font>", styles["BodyText"])
        try:
            image = Image(str(evidence_dir / photo.evidence_filename))
            image._restrictSize(16.5 * cm, 19 * cm)
            story.append(KeepTogether([caption, Spacer(1, 4), image, Spacer(1, 12)]))
        except Exception:
            story.extend([caption, Paragraph("Preview unavailable for this file type; see the evidence directory.", styles["BodyText"]), Spacer(1, 12)])
    document.build(story)
    return target
