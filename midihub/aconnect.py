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

__all__ = ('connectall', 'NotFound', 'NoConnections')

import re
import asyncio
from typing import List, Tuple, NamedTuple, Optional


clientRegex = re.compile(r"client (\d*)\:\s'((?:(?!client).)*)?'")
portRegex = re.compile(r"^\s+(\d+)\s")


Midi = NamedTuple("Midi", [("client", str), ("name", str), ("ports", List[str])])
MidiList = List[Midi]
MidiConnections = List[Tuple[str, str]]


class NotFound(Exception):
    pass


class NoConnections(Exception):
    pass


async def connect(from_port: str, to_port: str) -> Optional[str]:
    try:
        proc = await asyncio.create_subprocess_exec('aconnect', from_port, to_port,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)

        _, stderr = await proc.communicate()

        if stderr:
            return stderr.decode('utf8')
    except FileNotFoundError as err:
        raise NotFound from err


async def list() -> str:
    try:
        proc = await asyncio.create_subprocess_exec('aconnect', '-i', '-l',
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)

        stdout, _ = await proc.communicate()
        return stdout.decode('utf8')
    except FileNotFoundError as err:
        raise NotFound from err


def parse(input: str) -> MidiList:
    current = None
    devices: MidiList = []

    for line in input.splitlines():
        match = re.search(clientRegex, line)
        if match:
            client, name = match.groups()
            if re.search(r"Through", name) or client == '0':
                continue
            if current:
                devices.append(current)
            current = Midi(client, name, [])

        match = re.search(portRegex, line)
        if match and current is not None:
            port, = match.groups()
            current.ports.append(port)

    if current:
        devices.append(current)  # clear out last device

    return devices


def zip(devices: MidiList) -> MidiConnections:
    result = []
    for tx in devices:
        for rx in devices:
            for tx_port in tx.ports:
                for rx_port in rx.ports:
                    if tx.client == rx.client and tx_port == rx_port:
                        continue
                    result.append(
                        (f"{tx.client}:{tx_port}", f"{rx.client}:{rx_port}"))
    return result


async def connectall() -> None:
    connections = zip(parse(await list()))
    if connections:
        for tx_port, rx_port in connections:
            print(f"connecting: {tx_port} -> {rx_port}")
            err = await connect(tx_port, rx_port)
            if (err):
                print(err)
    else:
        raise NoConnections
