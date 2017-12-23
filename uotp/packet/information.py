from struct import unpack_from

from .base import Packet, Opcode


class InformationRequest(Packet):
    OPCODE = Opcode.Information

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        oid, seed, partner = map(lambda x: x.strip(), unpack_from('!11s40s80s', payload, 0))

        return {
            'oid': int(oid),
            'seeed': seed,
            'partner': partner,
        }
