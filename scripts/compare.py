import sys
import argparse
from os.path import abspath, dirname, exists, join, split, splitext
from PIL import Image, ImageDraw
from tylerd.platform.nes import Nes
import json


here = abspath(dirname(__file__))
list_txt = join(here, '..', 'assets', 'screens', 'list.txt')
screen_path = abspath(join(here, '..', 'assets', 'screens'))
output_path = abspath(join(here, '..', 'output'))


def compare_images(image_path1, image_path2, output='differences_marked.png', summary=True):
    if summary:
        file_path, file_name = split(output)
        name, _ = splitext(file_name)
        sumary_output_json = join(file_path, f'{name}.json')
        sumary_output_text = join(file_path, f'{name}.txt')
    
    # Open the images
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Convert images to RGB mode
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Define block sizes
    block_sizes = [(16, 16), (8, 8), (1, 1)]
    colors = [(255, 165, 0), (255, 255, 0), (255, 0, 0)]
    # block_sizes = [(8, 8)]
    # block_sizes = [(1, 1)]

    # Initialize a new image for marking differences
    diff_blocks = []
    nes = Nes()
    
    sumary_data = {}
    # Log differences and mark them in the diff image
    for block_size, color in zip(block_sizes, colors):
        miss = 0
        hit = 0
        for y in range(0, min(img1.height, img2.height), block_size[1]):
            for x in range(0, min(img1.width, img2.width), block_size[0]):
                is_diff = False
                for dy in range(block_size[1]):
                    for dx in range(block_size[0]):
                        px1 = img1.getpixel((x + dx, y + dy))
                        px2 = img2.getpixel((x + dx, y + dy))
                        c1 = nes.get_color_code(px1)
                        c2 = nes.get_color_code(px2)
                        if c1 != c2:
                            is_diff = True
                            diff_blocks.append((x, y, block_size, color))
                            break
                    if is_diff:
                        break
                if is_diff:
                    miss += 1
                else:
                    hit += 1
        sumary_data[block_size[0]] = dict(hit=hit, miss=miss)

    sumary_data['diff'] = diff_blocks
    if summary:
        with open(sumary_output_json, 'w') as fp:
            json.dump(sumary_data, fp)
        with open(sumary_output_text, 'w') as fp:
            fp.write(f'Metatiles hit: {sumary_data[16]["hit"]}\n')
            fp.write(f'Metatiles miss: {sumary_data[16]["miss"]}\n')
            fp.write(f'Tiles hit: {sumary_data[8]["hit"]}\n')
            fp.write(f'Tiles miss: {sumary_data[8]["miss"]}\n')
            fp.write(f'Pixels hit: {sumary_data[1]["hit"]}\n')
            fp.write(f'Pixels miss: {sumary_data[1]["miss"]}\n')

    # Create the difference image
    diff_img = Image.new('RGB', img1.size, color=(255, 255, 255))
    draw = ImageDraw.Draw(diff_img)
    for block in diff_blocks:
        x, y, block_size, color = block
        draw.rectangle([x, y, x + block_size[0], y + block_size[1]], fill=color)
    print(output)
    diff_img.save(output)

def auto():
    gamelist = []
    with open(list_txt, 'r') as fp:
        line = fp.readline()
        while line:
            title, filename = line.split(';')
            tag = filename.strip()[:-4]
            gamelist.append((title, tag))
            line = fp.readline()
    
    for title, tag in gamelist:
        asset_png = join(screen_path, f'{tag}.png')
        screenshot_png = join(output_path, f'{tag}_screenshot.png')
        diff_png = join(output_path, f'{tag}_diff.png')
        if exists(asset_png) and exists(screenshot_png):
            print(diff_png)
            compare_images(asset_png, screenshot_png, diff_png)



def main(argv):
    parser = argparse.ArgumentParser(description='Compare Images.')
    parser.add_argument("image1", type=argparse.FileType('r'), help="Path to the first image") 
    parser.add_argument("image2", type=argparse.FileType('r'), help="Path to the second image")

    parser.add_argument(
        '-o',
        '--output',
        metavar='OUTPUT_FILE',
        type=str,
        help='Output file name',
    )

    try:
        args = parser.parse_args(argv)
        image1_path = args.image1.name
        image2_path = args.image2.name
        output = args.output
        compare_images(image1_path, image2_path, output)

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    # auto()
    main(sys.argv[1:])
