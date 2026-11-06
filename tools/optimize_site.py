"""Build the light site art from the PNG sources: assets/site/**/*.webp and fonts/RobotoCondensed.woff2.

Run after the PNG art or the font changes:  python -X utf8 tools/optimize_site.py
Needs Pillow (with WebP) and brotli. The PNG files stay as the sources; the pages load only the WebP/WOFF2 files.
"""
from pathlib import Path
import io
import struct
import brotli
from PIL import Image

R = Path(__file__).resolve().parents[1]
SITE = R / 'assets/site'
ART = ['arm-base', 'arm-moving', 'spindle', 'turntable_plate']
QUALITY = 88


def webp_bytes(path):
    """Smaller of lossless and lossy WebP, unless lossless is already tiny (sprites keep exact edges)."""
    im = Image.open(path)
    im.load()
    lossless = io.BytesIO()
    im.save(lossless, 'WEBP', lossless=True, method=6)
    lossy = io.BytesIO()
    im.save(lossy, 'WEBP', quality=QUALITY, alpha_quality=100, method=6)
    a, b = lossless.getvalue(), lossy.getvalue()
    return a if len(a) <= 40_000 or len(a) <= 1.3 * len(b) else b


def hero_bytes(path):
    im = Image.open(path)
    im.load()
    out = io.BytesIO()
    im.save(out, 'WEBP', quality=85, alpha_quality=100, method=6)
    return out.getvalue()


KNOWN = ['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post', 'cvt ', 'fpgm', 'glyf', 'loca', 'prep', 'CFF ',
         'VORG', 'EBDT', 'EBLC', 'gasp', 'hdmx', 'kern', 'LTSH', 'PCLT', 'VDMX', 'vhea', 'vmtx', 'BASE', 'GDEF', 'GPOS',
         'GSUB', 'EBSC', 'JSTF', 'MATH', 'CBDT', 'CBLC', 'COLR', 'CPAL', 'SVG ', 'sbix', 'acnt', 'avar', 'bdat', 'bloc',
         'bsln', 'cvar', 'fdsc', 'feat', 'fmtx', 'fvar', 'gvar', 'hsty', 'just', 'lcar', 'mort', 'morx', 'opbd', 'prop',
         'trak', 'Zapf', 'Silf', 'Glat', 'Gloc', 'Feat', 'Sill']


def base128(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append(0x80 | (n & 0x7F))
        n >>= 7
    return bytes(reversed(out))


def woff2_bytes(ttf):
    """TrueType -> WOFF2 without glyph transforms (glyf/loca null transform, version 3); DSIG dropped."""
    data = Path(ttf).read_bytes()
    flavor, count = struct.unpack('>IH', data[:6])
    tables = []
    for i in range(count):
        tag, _, off, length = struct.unpack('>4sIII', data[12 + 16 * i:28 + 16 * i])
        tables.append((tag.decode('latin1'), data[off:off + length]))
    tables = sorted((t for t in tables if t[0] != 'DSIG'), key=lambda t: t[0])
    directory, stream, sfnt_size = b'', b'', 12 + 16 * len(tables)
    for tag, body in tables:
        version = 3 if tag in ('glyf', 'loca') else 0
        flags = (KNOWN.index(tag) if tag in KNOWN else 63) | (version << 6)
        directory += bytes([flags]) + (b'' if tag in KNOWN else tag.encode('latin1')) + base128(len(body))
        stream += body
        sfnt_size += (len(body) + 3) & ~3
    packed = brotli.compress(stream, quality=11, mode=brotli.MODE_FONT)
    total = (48 + len(directory) + len(packed) + 3) & ~3
    header = struct.pack('>4sIIHHIIHHIIIII', b'wOF2', flavor, total, len(tables), 0, sfnt_size, len(packed), 1, 0, 0, 0, 0, 0, 0)
    out = header + directory + packed
    return out + b'\0' * (total - len(out))


def main():
    sources = sorted((SITE / 'native').glob('*.png')) + [SITE / (n + '.png') for n in ART]
    total_png = total_webp = 0
    for png in sources:
        data = webp_bytes(png)
        png.with_suffix('.webp').write_bytes(data)
        total_png += png.stat().st_size
        total_webp += len(data)
    for lang in ('ru', 'de', 'en'):
        (SITE / ('peakmp3-' + lang + '.webp')).write_bytes(hero_bytes(SITE / ('peakmp3-' + lang + '.png')))
    font = SITE / 'fonts'
    (font / 'RobotoCondensed.woff2').write_bytes(woff2_bytes(font / 'RobotoCondensed.ttf'))
    print('demo art: %d KB PNG -> %d KB WebP' % (total_png // 1024, total_webp // 1024))
    print('font: %d KB TTF -> %d KB WOFF2' % ((font / 'RobotoCondensed.ttf').stat().st_size // 1024, (font / 'RobotoCondensed.woff2').stat().st_size // 1024))


if __name__ == '__main__':
    main()
