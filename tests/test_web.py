import unittest

from apartment_condition_report.web import _parse_multipart, _safe_filename


class WebTests(unittest.TestCase):
    def test_parse_multipart_reads_title_option_and_images(self) -> None:
        boundary = "test-boundary"
        body = (
            b"--test-boundary\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\nMove-in report\r\n"
            b"--test-boundary\r\nContent-Disposition: form-data; name=\"analyze\"\r\n\r\ntrue\r\n"
            b"--test-boundary\r\nContent-Disposition: form-data; name=\"photos\"; filename=\"room.jpg\"\r\nContent-Type: image/jpeg\r\n\r\nimage-bytes\r\n"
            b"--test-boundary--\r\n"
        )
        title, analyze, uploads = _parse_multipart(f"multipart/form-data; boundary={boundary}", body)
        self.assertEqual(title, "Move-in report")
        self.assertTrue(analyze)
        self.assertEqual([(upload.filename, upload.content) for upload in uploads], [("room.jpg", b"image-bytes")])

    def test_safe_filename_removes_client_paths_and_is_unique(self) -> None:
        self.assertNotIn("/", _safe_filename("../../room.jpg", 1))
        self.assertNotEqual(_safe_filename("room.jpg", 1), _safe_filename("room.jpg", 2))
