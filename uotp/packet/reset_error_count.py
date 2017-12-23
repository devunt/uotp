from .base import Packet, Opcode


class ResetErrorCountRequest(Packet):
    OPCODE = Opcode.ResetErrorCount

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        return {}
