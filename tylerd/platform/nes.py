from tylerd.platform.base import Platform
from tylerd.helper import hex_to_rgb, color_distance
from colr import color as colorf

# FCEMU
colors = [
    0x747474,
    0x24188C,
    0x0000A8,
    0x44009C,
    0x8C0074,
    0xA80010,
    0xA40000,
    0x7C0800,
    0x402C00,
    0x004400,
    0x005000,
    0x003C14,
    0x183C5C,
    0x000000,
    0x000000,
    0x000000,
    0xBCBCBC,
    0x0070EC,
    0x2038EC,
    0x8000F0,
    0xBC00BC,
    0xE40058,
    0xD82800,
    0xC84C0C,
    0x887000,
    0x009400,
    0x00A800,
    0x009038,
    0x008088,
    0x000000,
    0x000000,
    0x000000,
    0xFCFCFC,
    0x3CBCFC,
    0x5C94FC,
    0xCC88FC,
    0xF478FC,
    0xFC74B4,
    0xFC7460,
    0xFC9838,
    0xF0BC3C,
    0x80D010,
    0x4CDC48,
    0x58F898,
    0x00E8D8,
    0x000000,
    0x000000,
    0x000000,
    0xFCFCFC,
    0xA8E4FC,
    0xC4D4FC,
    0xD4C8FC,
    0xFCC4FC,
    0xFCC4D8,
    0xFCBCB0,
    0xFCD8A8,
    0xFCE4A0,
    0xE0FCA0,
    0xA8F0BC,
    0xB0FCCC,
    0x9CFCF0,
    0x000000,
    0x000000,
    0x000000,
]

colors_rgb = [hex_to_rgb(c) for c in colors]

BLACK = 0x0D


class Nes(Platform):
    def get_color_code(self, color):
        if color == (0, 0, 0):
            return BLACK
        elif color in colors_rgb:
            return colors_rgb.index(color)
        closest = sorted(colors_rgb, key=lambda c1: color_distance(color, c1))
        selected = [c for c in closest if c != (0, 0, 0)]

        color_index = colors_rgb.index(selected[0])

        if color_index in [
            0x0D,
            0x0E,
            0x0F,
            0x1D,
            0x1E,
            0x1F,
            0x2D,
            0x2E,
            0x2F,
            0x3D,
            0x3E,
            0x3F,
        ]:
            return BLACK

        return color_index

    def debug_screen(self, screen):
        vscan = int(len(screen) / 2)
        for vindex in range(vscan):
            line1 = screen[vindex * 2]
            line2 = screen[(vindex * 2) + 1]
            assert len(line1) == len(line2)
            str = ''
            for hindex in range(len(line1)):
                i1 = line1[hindex]
                i2 = line2[hindex]
                c1 = colors_rgb[i1]
                c2 = colors_rgb[i2]
                str += colorf('\u2592', fore=c2, back=c1)
            print(str)

    def has_metatiles(self):
        return True

    def get_tile_size(self):
        return 8

    def get_amount_colors_per_palette(self):
        return 4

    def get_amount_background_palettes(self):
        return 4

    def get_amount_sprite_palettes(self):
        return 4
    
    def color_code_to_rgb(self, code):
        return colors_rgb[code]
