from os.path import splitext
from PIL import Image
from functools import lru_cache


def str_bytes(_bytes, arrange=16):
    payload = ''
    for _slice in range(0, len(_bytes), arrange):
        chunk = _bytes[_slice : _slice + arrange]
        payload += ' .byte '
        payload += ', '.join(['$%02x' % byte for byte in chunk])
        payload += '\n'
    return payload


def hex_to_rgb(h):
    return h >> 16, (h >> 8) & 0xFF, h & 0xFF


@lru_cache(maxsize=None)
def color_distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2


def load_image(file, platform):
    # path, ext = splitext(file)
    # full_path = path.split('/')
    # filename = path if len(full_path) == 1 else path[-1]
    # _, filename = path.split('/')

    image = Image.open(file)

    return platform.get_width_height_screen(image)


def get_metatile(data, x, y):
    # mtile = [[0 for w in range(16)] for h in range(16)]
    mtile = []
    for py in range(16):
        for px in range(16):
            # mtile[py][px] = data[y * 16 + py][x * 16 + px]
            mtile.append(data[y * 16 + py][x * 16 + px])
    return mtile
