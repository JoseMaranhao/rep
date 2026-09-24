from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from apartment_condition_report.models import Finding, Photo
from apartment_condition_report.render import build_report


@unittest.skipUnless(find_spec("reportlab"), "reportlab is required to render PDF reports")
class ReportRenderingTests(unittest.TestCase):
    def test_builds_pdf_and_copies_evidence(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            tmp_path = Path(temporary_directory)
            photo = tmp_path / "wall.jpg"
            # ReportLab only needs a valid JPEG when it builds the document. This test uses a tiny valid JPEG fixture.
            photo.write_bytes(bytes.fromhex("ffd8ffe000104a46494600010100000100010000ffdb004300" + "08" * 64 + "ffc00011080001000103012200021101031101ffc40014000100000000000000000000000000000000ffc40014100100000000000000000000000000000000ffda000c03010002110311003f00ffd9"))
            result = build_report("Move-in report", [Finding("paint", "low", "Scuff", "hall", "high", "source", "evidence-wall.jpg")], 1, tmp_path / "report", [Photo(photo, "source", "evidence-wall.jpg")])
            self.assertEqual(result.name, "report.pdf")
            self.assertTrue(result.read_bytes().startswith(b"%PDF"))
            self.assertEqual((tmp_path / "report" / "evidence" / "evidence-wall.jpg").read_bytes(), photo.read_bytes())
