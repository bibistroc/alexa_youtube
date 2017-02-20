import unittest
from alexa.utils import config
from alexa.utils import youtube


class UtilsConfig(unittest.TestCase):
    def setUp(self):
        self.config = config.LocalConfig()

    def test_section_exists(self):
        self.assertNotEqual(self.config.general, None, "If the section exists, section is not None")

    def test_section_dont_exists(self):
        self.assertEqual(self.config.alabala, None, "If the section don't exist, section is None")

    def test_key_exists(self):
        self.assertNotEqual(self.config.general['name'], None, "If the key exists in section, key is not None")


class UtilsYoutube(unittest.TestCase):
    def setUp(self):
        self.youtube = youtube.Youtube()
        self.youtube.search('Du Hast')
        self.current = self.youtube.current()

    def test_current(self):
        self.assertTrue(isinstance(self.current, youtube.YoutubeVideoInformation))

    def test_current_url(self):
        self.assertNotEqual(self.current.stream_url.find('stream'), -1)

    def test_title(self):
        self.assertNotEqual(repr(self.current).find('Du Hast'), -1)

    def test_play_next(self):
        self.assertEqual(self.youtube.play_next(), self.youtube._Youtube__similar[0])

    def test_play_next_queue(self):
        self.youtube.play_next()
        self.youtube._Youtube__similar_index = 9
        self.youtube.play_next()
        self.assertEqual(self.youtube._Youtube__similar_index, 0)

    def test_play_prev(self):
        self.assertEqual(self.youtube.play_prev(), False)

    def test_play_prev_works(self):
        self.youtube.play_next()
        self.youtube.play_next()
        self.assertNotEqual(self.youtube.play_prev(), False)

    def test_clear(self):
        self.youtube.clear()
        self.assertEqual(len(self.youtube._candidates), 0)


