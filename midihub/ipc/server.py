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

import sys
import asyncio
import midihub.aconnect as aconnect
import midihub.ipc.message as message


async def handle_usb():
    print("usb device connected")
    try:
        await aconnect.connectall()
    except aconnect.NoConnections:
        print("no possible MIDI connections found")
    except aconnect.NotFound as _:
        print("aconnect not found", file=sys.stderr)


async def handle_message(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        body = await asyncio.wait_for(message.decode(reader), timeout=1.0)

        if body['type'] == 'usb':
            await handle_usb()

    except Exception as err:
        print(err)

    writer.close()
    await writer.wait_closed()


async def start():
    server = await asyncio.start_unix_server(handle_message, '/tmp/py-midihub.sock')

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start())
