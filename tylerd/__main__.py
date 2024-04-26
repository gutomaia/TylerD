import argparse
import sys
from tylerd.import_image import import_image


PLATFORM = ['nes']
FORMAT = ['nametable', '8bb']
FORMAT = ['2bpp', '2bpp_metatiles', '4bpp', '8bpp', '8bpp_direct_color']


def parser(argv):
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument(
        'image', metavar='FILE', type=str, help='The input file'
    )
    parser.add_argument(
        '-b',
        '--basename',
        metavar='BASENAME',
        type=str,
        help='Basename to use in the source',
    )
    parser.add_argument(
        '-o',
        '--output',
        metavar='OUTPUT_FILE',
        type=str,
        help='Output file name',
    )
    parser.add_argument(
        '-p',
        '--platform',
        metavar='TYPE',
        type=str,
        choices=PLATFORM,
        required=True,
        help='Platform. Choose from: ' + ', '.join(PLATFORM),
        default='nes',
    )
    parser.add_argument(
        '-f',
        '--format',
        metavar='TYPE',
        type=str,
        choices=FORMAT,
        required=True,
        help='Format of the file. Choose from: ' + ', '.join(FORMAT),
    )
    try:
        args = parser.parse_args(argv)
        basename = args.basename
        image = args.image
        output = args.output
        platform = args.platform
        format = args.format

        import_image(
            file=image,
            output=output,
            basename=basename,
            format=format,
            platform=platform,
        )

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


def main():
    parser(sys.argv[1:])


if __name__ == '__main__':
    main()
