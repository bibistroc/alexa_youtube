import unittest
from alexa.utils import config


class UtilsConfig(unittest.TestCase):
    def setUp(self):
        self.config = config.LocalConfig()

    def test_section_exists(self):
        self.assertNotEqual(self.config.general, None, "If the section exists, section is not None")

    def test_section_dont_exists(self):
        self.assertEqual(self.config.alabala, None, "If the section don't exist, section is None")

    def test_key_exists(self):
        self.assertNotEqual(self.config.general['name'], None, "If the key exists in section, key is not None")

    def test_key_dont_exists(self):
        try:
            self.config.general['alabala']
        except KeyError:
            pass
        except Exception, e:
            self.fail("ex: %s" % str(e))
