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

__all__ = ('connect_all')

import sys
import midihub.aconnect as aconnect


async def connect_all() -> None:
    try:
        await aconnect.connectall()
    except aconnect.NoConnections:
        print("no possible MIDI connections found")
    except aconnect.NotFound as _:
        print("aconnect not found", file=sys.stderr)
