import numpy as np
from colr import color as colorf

from tylerd.helper import (
    get_metatile,
    str_bytes,
    load_image,
    hex_to_rgb,
    color_distance,
)
from collections import Counter
from tylerd.platform.base import PlatformManager
from tylerd.platform.nes import colors, colors_rgb
from tylerd.core.strategies import HasFourMainPalettes, HasLessThenFourMainPalettes, HasMoreThenFourMainPalettes
from tylerd.core.palette import Palette


class Nametable:
    def __init__(self, image, debug = True):
        self.platform = PlatformManager()
        w, h, screen = load_image(image, self.platform)
        # self.platform.debug_screen(screen)
        self.colors = []
        self.sprite_colors = []

        if self.platform.uses_metatiles:
            self.meta_tiles = create_metatiles(w, h, screen)
            for mt in self.meta_tiles:
                self.colors.append(mt.colors)

        self.tile_palettes = []
        self.sprite_palettes = []
        self.__tiles_encoded = None

        self.discovery_metatiles_strategies = [
            HasFourMainPalettes(),
            HasLessThenFourMainPalettes(),
            HasMoreThenFourMainPalettes()
        ]

    def discover_metatiles_palette(self):
        palettes = [Palette(c)
                    for c in self.colors if len(c) == 4]
        other_palettes = [
            tuple(c) for c in self.colors if len(c) != 4
        ]
        scores = dict(Counter(palettes))

        palettes = []
        for palette, count in scores.items():
            palette.set_weight(count)
            palettes.append(palette)

        remaning_palettes = []
        over_colors = []
        for op in other_palettes:
            for pal in palettes:
                if len(op) > 4:
                    contains = pal.contains(op)
                    if len(contains) >= 3:
                        pal.inc_weight()
                        not_contains = pal.not_contains(op)
                        not_contains.sort()
                        over_colors.append(not_contains)
                    break
                elif pal.has(op):
                    pal.inc_weight()
                    break
            else:
                remaning_palettes.append(op)


        for strategy in self.discovery_metatiles_strategies:
            if strategy.is_applicable(palettes):
                strategy.apply(self, palettes)
                break

    def fix_palette(self):
        unknow = []
        for mt in self.meta_tiles:
            if mt.colors in self.tile_palettes:
                mt.colors = mt.colors
                mt.palette = mt.colors
            elif len(mt.colors) > 4:
                founds = []
                for pal in self.tile_palettes:
                    matches = {k: k in pal for k in mt.colors}
                    fill_screen = []
                    for tile in mt.tiles:
                        total = 0
                        for p in tile.original_data:
                            if p in pal:
                                total += 1
                        fill_screen.append(total)
                    founds.append(
                        (sum(matches.values()), sum(fill_screen), matches)
                    )
                # print('founds', founds)
                # matches = max(founds)[2]

                # sc = [k for k, v in matches.items() if v == False]
                # sc.sort()
                # mt.colors = pal
                # mt.palette = pal
                # mt.sprite_colors = sc
            else:
                for p in self.tile_palettes:
                    if all(item in p for item in mt.colors):
                        mt.colors = p
                        mt.palette = p
                        break
                else:
                    if mt.colors not in unknow:
                        unknow.append(mt.colors)
        return unknow

    @property
    def tile_encoded(self):
        if not self.__tiles_encoded:
            self.__tiles_encoded = []
            for mt in self.meta_tiles:
                for t in mt.tiles:
                    encoded = t.tile_encoded
                    if encoded not in self.__tiles_encoded:
                        self.__tiles_encoded.append(encoded)

            # TODO: print('number of tiles', len(encoded))

        return self.__tiles_encoded

    def chr(self):
        result = []
        for index, d in enumerate(self.tile_encoded):
            if index > 255:
                break
            result.extend(d)

        return result

    def iter_tiles(self):
        for line in range(14):
            for col in range(16):
                yield self.meta_tiles[col + line * 16].tiles[0]
                yield self.meta_tiles[col + line * 16].tiles[1]
            for col in range(16):
                yield self.meta_tiles[col + line * 16].tiles[2]
                yield self.meta_tiles[col + line * 16].tiles[3]

    def get_tile_index(self, id):
        index = self.tile_encoded.index(id)
        if index > 255:
            return 1
        return index

    def nam(self):
        nam = []
        for tile in self.iter_tiles():
            index = self.get_tile_index(tile.tile_id)
            if index < 256:
                nam.append(index)
            else:
                print('index larger: ', index)
        return nam

    def attr(self):
        attrs = []
        turn = 16
        for line in range(0, 14, 2):
            for col in range(0, 16, 2):
                indexes = [
                    col + (line * 16),
                    col + 1 + (line * 16),
                    col + turn + (line * 16),
                    col + turn + 1 + (line * 16),
                ]
                mts = [self.meta_tiles[i] for i in indexes]
                ta = [0, 0, 0, 0]
                for i, mt in enumerate(mts):
                    if mt.palette in self.tile_palettes:
                        ta_index = self.tile_palettes.index(mt.palette)
                        if ta_index >= 4:
                            ta[i] = 0
                        else:
                            ta[i] = ta_index
                    else:
                        print('pallete not found', mt.colors)
                        ta[i] = 1
                attr = ta[0] | (ta[1] << 2) | (ta[2] << 4) | (ta[3] << 6)
                attrs.append(attr)

        print(len(attrs))
        return attrs

    def chr_bytes(self):
        return str_bytes(self.chr())

    def palette_bytes(self):
        palette = []
        for p in self.tile_palettes:
            palette.extend(p.colors)
        return str_bytes(palette, 4)

    def nam_bytes(self):
        return str_bytes(self.nam())

    def attr_bytes(self):
        return str_bytes(self.attr())

    def nametable(self, basename, segment=None):
        chr_name = f'_{basename}_chr'
        pal_name = f'_{basename}_pal'
        nam_name = f'_{basename}_nam'
        attr_name = f'_{basename}_attr'
        payload = '.export '
        payload += ', '.join([pal_name, chr_name, nam_name, attr_name])
        payload += '\n'

        if segment:
            payload += f'.segment "${segment}"\n'
        payload += '\n'

        payload += f'\n{pal_name}:\n'
        payload += self.palette_bytes()

        payload += f'\n{chr_name}:\n'
        payload += self.chr_bytes()

        payload += f'\n{nam_name}:\n'
        payload += self.nam_bytes()

        payload += f'\n{attr_name}:\n'
        payload += self.attr_bytes()

        payload += '\n'
        return payload

    def debug_palettes(self):
        ch = bytes((219, 219)).decode('cp437')
        ptex = ''
        for p in self.palettes:
            for cr in p:
                rgb = hex_to_rgb(cr)
                ptex += colorf(ch, back=rgb, fore=rgb)
                ptex += ' '
                ptex += colorf(cr, back=rgb, fore=rgb)
                ptex += ' '
                ptex += '$%02x ' % cr
            ptex += '\n'
        print(ptex)

    def debug_nametable(self):
        line = 0
        l1 = []
        l2 = []
        for index, color_code in enumerate(self.iter_pixel()):
            if index % 16 == 0 and index != 0:
                line += 1
            rgb = self.platform.color_code_to_rgb(color_code)
            if line % 2 == 0:
                l1.append(rgb)
            else:
                l2.append(rgb)
            if index % 32 == 0 and index != 0:
                str = ''
                for i in range(16):
                    str += colorf('\u2592', fore=l2[i], back=l1[i])
                l1 = []
                l2 = []
                print(str)

class Tile:
    def __init__(self, data):
        self.original_colors = list(set(data))
        self.original_colors.sort()
        self.original_data = data

        self.__tile_color_data = data
        self.__tile_palette_data = None
        self.__tile_id = None
        self.__tile_colors = None
        self.__tile_palette = None
        self.__tile_encoded = None

        self.__sprite_color_data = False
        self.__sprite_palette_data = None
        self.__sprite_id = None
        self.__sprite_colors = None
        self.__sprite_palette = None
        self.__sprite_encoded = None

    def get(self, x, y):
        return self.data[y * 8 + x]

    @property
    def tile_id(self):
        if not self.__tile_id:
            self.__tile_id = self.tile_encoded
        return self.__tile_id

    @property
    def tile_colors(self):
        return self.__tile_colors

    @tile_colors.setter
    def tile_colors(self, colors):
        assert len(colors) <= 4
        self.__tile_colors = colors
        self.__tile_color_data = []
        replace = {}
        distances = []
        colors_not_found = [
            c for c in self.original_colors if c not in self.__tile_colors
        ]
        for c1 in colors_not_found:
            distances = []
            for c2 in self.__tile_colors:
                distances.append(
                    (color_distance(colors_rgb[c1], colors_rgb[c2]), c2)
                )
                c3 = min(distances)[1]
                replace[c1] = c3

        self.__tile_color_data = []
        for d in self.original_data:
            if d in colors:
                self.__tile_color_data.append(d)
            else:
                self.__tile_color_data.append(replace[d])

        return self.__tile_colors

    @property
    def tile_color_data(self):
        return self.__tile_color_data

    @property
    def tile_palette(self):
        return self.__tile_palette

    @tile_palette.setter
    def tile_palette(self, palette: Palette):
        if not self.__tile_palette:
            self.__tile_palette = palette
            # self.__tile_palette_data = self.__tile_color_data
        self.__tile_palette = palette

    @property
    def tile_palette_data(self):
        if not self.__tile_palette_data:
            replace = {}
            distances = []
            colors_not_found = self.tile_palette.not_contains(self.tile_color_data)
            for c1 in colors_not_found:
                distances = []
                for c2 in self.tile_palette.colors:
                    distances.append(
                        (color_distance(colors_rgb[c1], colors_rgb[c2]), c2)
                    )
                c3 = min(distances)[1]
                replace[c1] = c3

            self.__tile_palette_data = []
            for d in self.tile_color_data:
                if d in colors_not_found:
                    self.__tile_palette_data.append(replace[d])
                else:
                    self.__tile_palette_data.append(d)

        return self.__tile_palette_data

    @property
    def tile_encoded(self):
        if not self.__tile_encoded:
            self.__tile_encoded = self.encode(
                self.tile_palette, self.tile_palette_data
            )
        return self.__tile_encoded

    @property
    def sprite_id(self):
        if not self.__tile_id:
            self.__id = self.sprite_encoded
        return self.__tile_id

    @property
    def sprite_colors(self):
        return self.__sprite_colors

    @property
    def sprite_encoded(self):
        if not self.__sprite_encoded:
            self.__sprite_encoded = self.encode(
                self.sprite_palette, self.sprite_palette_data
            )
        return self.__sprite_encoded

    def encode(self, palette, data):
        channel_a = []
        channel_b = []
        indexed_data = [palette.colors.index(d) for d in data]

        tile = np.array(indexed_data).reshape(8, 8)
        for y in range(8):
            a = 0
            b = 0
            for x in range(8):
                pixel = tile[y][x]
                bit = pow(2, 7 - x)
                if pixel == 1:
                    a = a | bit
                elif pixel == 2:
                    b = b | bit
                elif pixel == 3:
                    a = a | bit
                    b = b | bit
            channel_a.append(a)
            channel_b.append(b)
        return channel_a + channel_b

    def bytes_tiles(self):
        return str_bytes(self.encoded_tyles)

    def bytes_sprites(self):
        return str_bytes(self.encoded_sprites)


class MetaTile:
    def __init__(self, data):
        colors = list(set(data))
        colors.sort()
        self.__colors = tuple(colors)
        self.__palette = None

        self.define_tiles(data)

    def define_tiles(self, data):
        self.tiles = []
        metatiles = np.array(data).reshape(16, 16)
        for y, x in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            tile = []
            for py in range(8):
                for px in range(8):
                    tile.append(metatiles[y * 8 + py][x * 8 + px])
            tile = Tile(tile)
            self.tiles.append(tile)

    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, colors):
        if isinstance(colors, list):
            colors.sort()
            colors = tuple(colors)
        self.__colors = colors
        for t in self.tiles:
            t.tile_colors = colors

    @property
    def palette(self):
        return self.__palette

    @palette.setter
    def palette(self, value):
        self.__palette = value
        for t in self.tiles:
            t.tile_palette = value

    def iter_pixel(self):
        for y in range(8):
            for x in range(8):
                yield self.tiles[0].get(x, y)
                yield self.tiles[1].get(x, y)

        for y in range(8):
            for x in range(8):
                yield self.tiles[2].get(x, y)
                yield self.tiles[3].get(x, y)

    def debug(self):
        c = bytes((219,)).decode('cp437')
        mtile = ''
        for index, color_index in enumerate(self.iter_pixel()):
            if index % 16 == 0 and index != 0:
                mtile += '\n'
            rgb = hex_to_rgb(colors[color_index])
            mtile += self.colorf(c, back=rgb, fore=rgb)
        print(mtile)

    def to_ascii(self):
        line = 0
        l1 = []
        l2 = []
        mt = []
        for index, color_code in enumerate(self.iter_pixel()):
            if index % 16 == 0 and index != 0:
                line += 1
            rgb = self.platform.color_code_to_rgb(color_code)
            if line % 2 == 0:
                l1.append(rgb)
            else:
                l2.append(rgb)
            if index % 32 == 0 and index != 0:
                str = ''
                for i in range(16):
                    str += colorf('\u2592', fore=l2[i], back=l1[i])
                l1 = []
                l2 = []
                mt.append(str)
        return mt

def create_metatiles(w, h, screen):
    meta_tiles = []

    assert w % 16 == 0
    assert h % 16 == 0

    meta_w = w / 16
    meta_h = h / 16

    for y in range(14):
        for x in range(16):
            mtile = MetaTile(get_metatile(screen, x, y))
            meta_tiles.append(mtile)

    return meta_tiles
