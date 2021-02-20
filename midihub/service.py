#!/usr/bin/env python3
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

__all__ = ('start')

import sys
import asyncio
from asyncio.streams import StreamReader, StreamWriter
import midihub.aconnect as aconnect
import midihub.message as message
from enum import Enum
from typing import NamedTuple


class ClientType(Enum):
    Notify = "notify"
    Monitor = "monitor"


Client = NamedTuple("Client", [("type", ClientType),
                               ("reader", StreamReader), ("writer", StreamWriter)])


async def handle_usb():
    print("usb device connected")
    try:
        await aconnect.connectall()
    except aconnect.NoConnections:
        print("no possible MIDI connections found")
    except aconnect.NotFound as _:
        print("aconnect not found", file=sys.stderr)


async def handle_connected(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"connected to {addr}")
    try:
        # Looping like this should allow multiple clients
        while True:
            msg = await asyncio.wait_for(message.decode(reader), 2.0)
            if msg['type'] == 'usb':
                await handle_usb()
                break  # kludge, need to break loop because a notification fires and disconnects

    except asyncio.TimeoutError:
        print('connection timed out')
    except Exception as e:
        print(e)

    writer.close()
    await writer.wait_closed()


async def start():
    server = await asyncio.start_server(handle_connected, '127.0.0.1', 5432)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


# Read more thoroughly
# https://stackoverflow.com/questions/43393764/python-3-6-project-structure-leads-to-runtimewarning
if __name__ == "__main__":
    asyncio.run(start())
