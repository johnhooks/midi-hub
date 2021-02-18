from midihub.aconnect import Midi

data = {
    "aconnect": {
        "raw": {
            "basic": "client 0: 'System' [type=kernel]\n  0 'Timer           '\n  1 'Announce        '\nclient 14: 'Midi Through' [type=kernel]\n  0 'Midi Through Port-0'\nclient 16: 'Keystation Mini 32' [type=kernel]\n  0 'Keystation Mini 32 MIDI 1'\nclient 20: 'E-MU XMidi1X1' [type=kernel]\n  0 'E-MU XMidi1X1 MIDI 1'",
            "single_connection": "client 0: 'System' [type=kernel]\n  0 'Timer           '\n  1 'Announce        '\nclient 14: 'Midi Through' [type=kernel]\n  0 'Midi Through Port-0'\nclient 16: 'Keystation Mini 32' [type=kernel]\n  0 'Keystation Mini 32 MIDI 1'\nConnecting To: 20:0\nclient 20: 'E-MU XMidi1X1' [type=kernel]\n  0 'E-MU XMidi1X1 MIDI 1'\nConnected From: 16:0"
        },
        "parsed": {
            "basic": [Midi("16", "Keystation Mini 32", ["0"]), Midi("20", "E-MU XMidi1X1", ["0"])],
        },
        "zipped": {
            "basic": [("16:0", "20:0"), ("20:0", "16:0")]
        }
    }
}
