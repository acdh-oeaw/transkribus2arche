import unittest

from transkribus2arche.utils import read_json, get_md_dict


path_to_config = './transkribus2arche/config_sample.json'
trans_doc = './transkribus2arche/trp.json'


class TestUtirls(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_smoke(self):
        self.assertIsInstance("hansi4ever", str)

    def test_002_read_json(self):
        data = read_json(path_to_config)
        self.assertIsInstance(data, dict)

    def test_003_get_md_dict(self):
        item = get_md_dict(trans_doc, path_to_config)
        self.assertIsInstance(item, dict)
