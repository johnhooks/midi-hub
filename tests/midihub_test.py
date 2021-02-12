import unittest
from unittest import mock

from midihub import connectall, list_devices, zip

mock_aconnect_output = """client 0: 'System' [type=kernel]
    0 'Timer           '
    1 'Announce        '
client 14: 'Midi Through' [type=kernel]
    0 'Midi Through Port-0'
client 16: 'Keystation Mini 32' [type=kernel]
    0 'Keystation Mini 32 MIDI 1'
client 20: 'E-MU XMidi1X1' [type=kernel]
    0 'E-MU XMidi1X1 MIDI 1'
"""

mock_aconnect_output_connected = """client 0: 'System' [type=kernel]
    0 'Timer           '
    1 'Announce        '
client 14: 'Midi Through' [type=kernel]
    0 'Midi Through Port-0'
client 16: 'Keystation Mini 32' [type=kernel]
    0 'Keystation Mini 32 MIDI 1'
 Connecting To: 20:0
client 20: 'E-MU XMidi1X1' [type=kernel]
    0 'E-MU XMidi1X1 MIDI 1'
 Connected From: 16:0
"""


class TestConnectall(unittest.TestCase):
    @mock.patch('subprocess.Popen')
    def test_list_devices(self, mock_subproc_popen):
        process_mock = mock.MagicMock()
        attrs = {'communicate.return_value': (
            mock_aconnect_output, ""), 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        devices = list_devices()
        self.assertTrue(mock_subproc_popen.called)
        # https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
        self.assertEqual(["16", "20"], [*devices])


if __name__ == '__main__':
    unittest.main()
