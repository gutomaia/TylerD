import argparse
import sys
from PIL import Image
from tylerd.platform.nes import Nes


nes = Nes()


def get_attr_index(index):
    col = index % 32 // 4
    row = index // 32 // 4

    # Calculate the attribute index
    attribute_index = row * 8 + col
    return attribute_index

def get_palette(index, palettes):
    start = index * 4
    pal = palettes[start: start+4]
    return [nes.color_code_to_rgb(p) for p in pal]

def get_palette_attr(index, attr, palettes):
    # Calculate the attribute index
    attribute_index = get_attr_index(index)

    # Extract the attribute byte from the nametable
    attribute_byte = attr[attribute_index]  # Attribute table starts at VRAM address $03C0 (960 in decimal)

    # Calculate the palette index based on the tile position within the attribute block
    tile_col = (index % 32) % 4
    tile_row = (index // 32) % 4
    palette_shift = (tile_row // 2) * 4 + (tile_col // 2) * 2
    palette_index = (attribute_byte >> palette_shift) & 0b11

    return get_palette(palette_index, palettes)

def get_sprite(index, sprites, palette):
    iA = index * 16
    iB = iA + 8
    iC = iB + 8
    channelA = sprites[iA:iB]
    channelB = sprites[iB:iC]
    s = []
    for y in range(0, 8):
        ca = channelA[y]
        cb = channelB[y]
        line = []
        for x in range(0, 8):
            bit = pow(2, 7 - x)
            if (not (ca & bit) and not (cb & bit)):
                code = 0
            elif ((ca & bit) and not (cb & bit)):
                code = 1
            elif (not (ca & bit) and (cb & bit)):
                code = 2
            elif ((ca & bit) and (cb & bit)):
                code = 3
            else:
                raise Exception()
            try:
                color = palette[code]
            except IndexError:
                color = palette[-1]
            line.append(color)
        s.append(line)
    return s

def emulate(file_s, output='emulated.png'):
    data = {}
    with open(file_s, 'r') as fp:
        exports = []
        line = fp.readline()
        current = None
        while line:
            line = line.strip()
            if line.startswith('.export '):
                exports = [e.strip() for e in line[8:].split(',')]
            elif line.startswith('.byte '):
                if current:
                    bytes_str = line[6:].split(',')
                    bytes_int = [int(b.strip()[1:], 16) for b in bytes_str]
                    data[current].extend(bytes_int)
            else:
                for export in exports:
                    if line.startswith(export):
                        current = export
                        data[current] = []
                        break
            line = fp.readline()

    palettes = None
    nametable = None
    tiles = None
    attr = None

    for k, v in data.items():
        if k.endswith('_pal'):
            palettes = v
        elif k.endswith('_nam'):
            nametable = v
        elif k.endswith('_chr'):
            tiles = v
        elif k.endswith('_attr'):
            attr = v

    image_width = 256
    image_height = 240
    image = Image.new("RGB", (image_width, image_height))
    for index, chr in enumerate(nametable):
        palette = get_palette_attr(index, attr, palettes)
        tile = get_sprite(chr, tiles, palette)
        tile_x = (index % 32) * 8
        tile_y = (index // 32) * 8
        for y in range(8):
            for x in range(8):
                image.putpixel((tile_x + x, tile_y + y), tile[y][x])
    image.save(output)


def main(argv):
    parser = argparse.ArgumentParser(description='Emulate Screen.')
    parser.add_argument("file_s", type=argparse.FileType('r'), help="Path to file s") 

    parser.add_argument(
        '-o',
        '--output',
        metavar='OUTPUT_FILE',
        type=str,
        help='Output file name',
    )

    try:
        args = parser.parse_args(argv)
        emulate(args.file_s.name, args.output)

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
