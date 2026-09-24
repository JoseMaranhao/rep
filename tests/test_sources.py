from pathlib import Path
import unittest

from apartment_condition_report.sources import local_photos


class LocalPhotosTests(unittest.TestCase):
    def test_recurses_and_filters_images(self) -> None:
        with self.subTest("images are recursive and deterministic"):
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as temporary_directory:
                tmp_path = Path(temporary_directory)
                (tmp_path / "nested").mkdir()
                (tmp_path / "a.JPG").write_bytes(b"image")
                (tmp_path / "nested" / "b.png").write_bytes(b"image")
                (tmp_path / "notes.txt").write_text("not an image")
                self.assertEqual([photo.path.name for photo in local_photos(tmp_path)], ["a.JPG", "b.png"])
