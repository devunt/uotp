from .base import Packet, Opcode


class HelpRequest(Packet):
    OPCODE = Opcode.Help

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        payload = payload[:-8].decode('cp949')
        return {
            'messages': payload.split('|'),
        }
