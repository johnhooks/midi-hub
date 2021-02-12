# Copyright (C) 2021 copyright-holder John Hooks <bitmachina@outlook.com>
# This file is part of midi-hub.
#
# midi-hub is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# midi-hub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with midi-hub.  If not, see <https://www.gnu.org/licenses/>.

import re
import sys
import subprocess
from typing import Dict, List, Tuple


listRegex = re.compile(r"client (\d*)\:\s'((?:(?!client).)*)?'")
portRegex = re.compile(r"^\s+(\d+)\s")


def zip(devices: Dict[str, Tuple[str, List[str]]]) -> List[Tuple[str, str, str, str]]:
    result = []
    for tx_id in devices.keys():
        for rx_id in devices.keys():
            tx_name, tx_ports = devices[tx_id]
            rx_name, rx_ports = devices[rx_id]
            for tx_port in tx_ports:
                for rx_port in rx_ports:
                    if tx_id == rx_id and tx_port == rx_port:
                        continue
                    result.append(
                        (tx_name, f"{tx_id}:{tx_port}", rx_name, f"{rx_id}:{rx_port}"))
    return result


def aconnect(from_port: str, to_port: str):
    proc = subprocess.Popen(['aconnect', from_port, to_port],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE,
                            text=True)
    if proc.returncode != 0:
        _, stderr = proc.communicate()
        print(stderr)


def list_devices() -> Dict[str, Tuple[str, List[str]]]:
    device = None
    devices: Dict[str, List[str]] = {}
    proc = subprocess.Popen(['aconnect', '-i', '-l'],
                            stdout=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        return {}
    stdout, _ = proc.communicate()
    for line in stdout.splitlines():
        match = re.search(listRegex, line)
        if match is not None:
            id, name = match.groups()
            if re.search(r"Through", name) is not None or id == '0':
                continue
            device = id
            devices[device] = (name, [])
        match = re.search(portRegex, line)
        if match is not None and device is not None and devices[device] is not None:
            port, = match.groups()
            devices[device][1].append(port)
    return devices


def connectall() -> None:
    try:
        connections = zip(list_devices())
        if not connections:
            print("no possible MIDI connections found")
        else:
            for _, tx_port, _, rx_port in zip(list_devices()):
                print(f"connecting: {tx_port} -> {rx_port}")
                aconnect(tx_port, rx_port)
    except FileNotFoundError as _:
        print("aconnect not found", file=sys.stderr)
