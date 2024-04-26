import argparse
import sys
from os.path import abspath, dirname, join
from jinja2 import Environment, FileSystemLoader


here = abspath(dirname(__file__))
templates_path = abspath(join(here, 'templates'))


def generate_source(name, output):
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template('cc65_nametable.c')

    rendered_content = template.render(name=name)
    with open(output, 'w') as f:
        f.write(rendered_content)


def main(argv):
    parser = argparse.ArgumentParser(description='Generate source.')

    # Adding the optional output argument
    parser.add_argument(
        '-o',
        '--output',
        metavar='OUTPUT_FILE',
        type=str,
        help='Output file name',
    )

    parser.add_argument(
        '-b', '--basename', metavar='NAME', type=str, help='Name file name'
    )

    try:
        args = parser.parse_args(argv)

        generate_source(args.basename, args.output)

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
