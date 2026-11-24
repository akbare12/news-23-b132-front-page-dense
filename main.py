"""news-23 b132 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Validates the PNG header manually (struct): signature, IHDR 13 bytes 1024x1024,
bit depth 8, colour type 2/6, compression/filter/interlace 0, IHDR CRC, per-chunk CRCs,
non-empty IDAT payload, IEND 0-byte as the last chunk with no trailing data.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_W = 1024
EXPECTED_H = 1024
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024
MIN_IDAT_PAYLOAD = 1000


def fail(msg):
    print("error: %s" % msg, file=sys.stderr)
    return 1


def main():
    repo = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(repo, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo_abs = os.path.abspath(repo)
    if os.path.commonpath([out_dir_abs, repo_abs]) == repo_abs:
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s"
                    % out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory: %s"
                    % out_dir)
    if not os.path.isfile(src):
        return fail("source entry.png not found: %s" % src)
    data = open(src, "rb").read()
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png too large: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes: width, height, bit depth,
    # colour type, compression, filter, interlace.
    # Layout: 8 signature | 4 length | 4 "IHDR" | 13 data | 4 CRC.
    if len(data) < 33:
        return fail("PNG too short for IHDR")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        return fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype, comp, filt, inter = struct.unpack(
        ">IIBBBBB", data[16:29])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        return fail("dimensions %dx%d, expected 1024x1024" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        return fail("bit depth %d / colour type %d unsupported"
                    % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        return fail("compression/filter/interlace must be 0")
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != ihdr_crc:
        return fail("IHDR CRC mismatch")
    # Walk the remaining chunks: length + type + data + CRC each.
    # Chunk layout: 4 length | 4 type | <length> data | 4 CRC.
    # The first chunk after IHDR therefore starts at offset 33
    # (8 signature + 4 length + 4 type + 13 data + 4 CRC = 33).
    pos = 33  # next chunk starts right after the IHDR CRC
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return fail("truncated chunk header at offset %d" % pos)
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype_b = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            return fail("truncated chunk %r" % ctype_b)
        crc_stored = struct.unpack(">I", data[end - 4:end])[0]
        crc_calc = zlib.crc32(ctype_b + data[pos + 8:pos + 8 + clen])
        crc_calc &= 0xFFFFFFFF
        if crc_calc != crc_stored:
            return fail("CRC mismatch in chunk %r" % ctype_b)
        if ctype_b == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            idat_total += clen
        if ctype_b == b"IEND":
            if clen != 0:
                return fail("IEND must be 0 bytes")
            if end != len(data):
                return fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return fail("no IEND chunk found")
    if idat_total < MIN_IDAT_PAYLOAD:
        return fail("IDAT payload too small: %d bytes" % idat_total)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source entry.png")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    back = open(dst, "rb").read()
    if back != data:
        return fail("output differs from source after copy")
    print("ok: wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
