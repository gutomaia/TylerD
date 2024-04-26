from tylerd.base import Nametable
from tylerd.platform import Nes
from tylerd.platform.base import PlatformManager


def import_image(file, output, basename, platform, format):
    p = None

    pm = PlatformManager()
    if platform == 'nes':
        pm.set_platform(Nes())

    nt = Nametable(file)
    nt.discover_metatiles_palette()

    with open(output, 'w') as f:
        f.write(nt.nametable(basename))

    # output = Image.new('RGB', (w, h))
    # output.putdata([colors_rgb[d] for d in data])
    # output.save('output.png')
