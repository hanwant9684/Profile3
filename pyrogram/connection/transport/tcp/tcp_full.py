#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging
from binascii import crc32
from struct import pack, unpack
from typing import Optional, Tuple

from .tcp import TCP, Proxy

log = logging.getLogger(__name__)


class TCPFull(TCP):
    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        super().__init__(ipv6, proxy)

        self.seq_no: Optional[int] = None
        self._send_buffer = bytearray(512 * 1024 + 64) # Pre-allocate 512KB + header space

    async def connect(self, address: Tuple[str, int]) -> None:
        await super().connect(address)
        self.seq_no = 0

    async def send(self, data: bytes, *args) -> None:
        # NITRO: Optimized single-buffer zero-copy send
        data_len = len(data)
        total_len = data_len + 12
        
        # Structure the payload in our pre-allocated buffer if it fits
        if total_len <= len(self._send_buffer):
            view = memoryview(self._send_buffer)
            # Length (4 bytes)
            view[0:4] = pack("<I", total_len)
            # Sequence Number (4 bytes)
            view[4:8] = pack("<I", self.seq_no)
            # Data
            view[8:8+data_len] = data
            # CRC32 of everything before the checksum
            checksum = crc32(view[0:8+data_len])
            view[8+data_len:12+data_len] = pack("<I", checksum)
            
            await super().send(view[0:total_len])
        else:
            # Fallback for jumbo packets (unlikely in Telegram)
            payload = pack("<II", total_len, self.seq_no) + data
            payload += pack("<I", crc32(payload))
            await super().send(payload)
        
        self.seq_no += 1

    async def recv(self, length: int = 0) -> Optional[bytes]:
        length = await super().recv(4)

        if length is None:
            return None

        packet = await super().recv(unpack("<I", length)[0] - 4)

        if packet is None:
            return None

        packet = length + packet
        checksum = packet[-4:]
        packet = packet[:-4]

        if crc32(packet) != unpack("<I", checksum)[0]:
            return None

        return packet[8:]
