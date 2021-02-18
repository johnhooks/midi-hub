import unittest

from midihub.aconnect import parse, zip
import midihub.tests.mock as mock


class TestAconnect(unittest.TestCase):

    def test_parse_raw(self):
        expected = mock.data['aconnect']['parsed']['basic']
        result = parse(mock.data['aconnect']['raw']['basic'])
        self.assertEqual(result, expected)

    def test_zip_devices(self):
        expected = mock.data['aconnect']['zipped']['basic']
        result = zip(mock.data['aconnect']['parsed']['basic'])
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
