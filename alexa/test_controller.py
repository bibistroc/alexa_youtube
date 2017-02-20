import unittest
import alexa


class Controller(unittest.TestCase):
    def setUp(self):
        self.app = alexa.app.test_client()

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK', "When / is accessed, HTTP 200 OK status is sent")

    @unittest.skip("showing class skipping")
    def test_stream(self):
        result = self.app.get('stream/W3q8Od5qJio.mp3')
        self.assertEqual(result.status, '200 OK',
                         "When /stream/<youtube_video_id>.mp3 is accessed, HTTP 200 OK status is sent")
