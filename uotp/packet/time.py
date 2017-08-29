from struct import unpack

from .base import Packet, Opcode


class TimeRequest(Packet):
    def __init__(self):
        super().__init__()
        self.opcode = Opcode.Time

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        time, = unpack("!I", payload)

        return {
            'time': time
        }
