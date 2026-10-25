from PIL import Image
import struct, sys

src, w, h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
img = Image.open(src).convert("RGB").resize((w, h))

out = bytearray()
for r, g, b in img.getdata():
    # pack to 16-bit RGB565, high byte first (what the screen expects)
    out += struct.pack(">H", ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3))

open(src.rsplit(".", 1)[0] + ".raw", "wb").write(out)