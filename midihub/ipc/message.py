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
import json
from asyncio import StreamReader
from typing import Any


content_length_regex = re.compile(r"^\s*Content-Length:\s*(\d+)\s$")


async def parse_body(reader: StreamReader, headers: dict):
    content_length = headers['Content-Length']
    bytes_read = 0
    raw = b''

    while bytes_read != content_length:
        chunk = await reader.read(content_length)
        if chunk:
            bytes_read += len(chunk)
            raw += chunk
        else:
            raise Exception('socket closed before reaching the end')

    try:
        return json.loads(raw)
    except json.JSONDecodeError as _:
        raise Exception('unable to parse body')


async def parse_headers(reader: StreamReader) -> dict:
    content_length: int

    while True:
        line = await reader.readline()
        if not line or line == b'\n':
            break
        match = re.search(content_length_regex, line.decode('utf8'))
        if match:
            length, = match.groups()
            try:
                content_length = int(length)
            except ValueError:
                raise Exception('invalid Content-Length header')

    if not content_length:
        raise Exception('invalid request headers')

    return {'Content-Length': content_length}


async def decode(reader: StreamReader) -> Any:
    headers = await parse_headers(reader)
    body = await parse_body(reader, headers)
    return body


def encode(data) -> bytes:
    body = json.dumps(data).encode('utf8')
    header = f'Content-Length: {len(body)}\n\n'.encode('utf8')
    return header + body
