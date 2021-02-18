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

import os
import sys
import json
import asyncio


async def notify_usb():
    try:
        _, writer = await asyncio.open_unix_connection('/tmp/py-midihub.sock')
        body = json.dumps({"type": "usb"}).encode('utf8')
        header = f'Content-Length: {len(body)}\n\n'.encode('utf8')
        writer.write(header + body)
        await asyncio.wait_for(writer.drain(), 1.0)
        writer.close()
        await writer.wait_closed()

    except (ConnectionRefusedError, FileNotFoundError) as _:
        sys.stderr.write('midi-hub service unavailable\n')
        sys.exit(os.EX_UNAVAILABLE)
    except asyncio.TimeoutError as _:
        sys.stderr.write('connection to midi-hub service timed out\n')
        sys.exit(os.EX_IOERR)


if __name__ == "__main__":
    asyncio.run(notify_usb())
