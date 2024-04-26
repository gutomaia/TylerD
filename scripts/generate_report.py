import argparse
from os.path import abspath, dirname, exists, join, relpath
import pytablewriter as ptw
import json


here = abspath(dirname(__file__))
list_txt = join(here, '..', 'assets', 'screens', 'list.txt')
screen_path = abspath(join(here, '..', 'assets', 'screens'))
output_path = abspath(join(here, '..', 'output'))

docs_path = abspath(join(here, '..', 'docs'))
gamelist_rst = join(docs_path, 'gamelist.rst')
imagelist_rst = join(docs_path, 'imagelist.rst')
results_rst = join(docs_path, 'results.rst')

def main():
    gamelist = []
    with open(list_txt, 'r') as fp:
        line = fp.readline()
        while line:
            title, filename = line.split(';')
            tag = filename.strip()[:-4]
            gamelist.append((title, tag))
            line = fp.readline()
    
    data_list = []
    results = []
    detail_filename = None
    detail_fp = None
    current = None
    mt_total_miss = 0
    mt_total_hits = 0
    for title, tag in gamelist:
        asset_png = join(screen_path, f'{tag}.png')
        emulated_png = join(output_path, f'{tag}_emulated.png')
        diff_png = join(output_path, f'{tag}_diff.png')
        screenshot_png = join(output_path, f'{tag}_screenshot.png')
        if exists(asset_png) and exists(emulated_png) and exists(screenshot_png):
            if not current or current != title[0].lower():
                current = title[0].lower()
                detail_filename = join(docs_path, f'results_{current}.rst')
                if detail_fp:
                    detail_fp.close()
                detail_fp = open(detail_filename, 'w')
                page_title = f'Results {current}'
                detail_fp.write(f'{page_title}\n')
                detail_fp.write('=' * len(page_title) + '\n\n')

            # with open()
            detail_fp.write(f'.. _{tag}:\n\n')
            detail_fp.write(f'{title}\n')
            detail_fp.write('=' * len(title) + '\n')
            detail_fp.write('\n')
            writer = ptw.RstGridTableWriter(
                # table_name="Result Details",
                headers=["Original", "Emulated", "FCEUX Screenshot"],
                value_matrix=[
                [
                    f".. image:: ../assets/screens/{tag}.png",
                    f".. image:: ../output/{tag}_emulated.png",
                    f".. image:: ../output/{tag}_screenshot.png",
                    # f".. image:: ../output/{tag}_diff.png",
                ]
            ])
            detail_fp.write(writer.dumps())
            detail_fp.write('\n')
            detail_fp.write('.. raw:: html\n')
            detail_fp.write('\n')
            detail_fp.write('    <div style="display: flex; align-items: center;">\n')
            detail_fp.write('\n')
            detail_fp.write(f".. image:: ../output/{tag}_diff.png\n")
            # detail_fp.write("   :width:100px\n")
            # detail_fp.write("   :align:left\n")
            # detail_fp.write("   :border:1px\n")
            detail_fp.write('\n')
            detail_fp.write(f'.. literalinclude:: ../output/{tag}_diff.txt\n')
            detail_fp.write('   :language: rst\n')
            detail_fp.write('   :linenos:\n')
            detail_fp.write('   :emphasize-lines: 2,4,6\n')
            detail_fp.write('\n')
            detail_fp.write('.. raw:: html\n')
            detail_fp.write('\n')
            detail_fp.write('    </div>\n')
            detail_fp.write('\n')
            detail_fp.write('\n')

            report = {}
            with open(join(output_path, f'{tag}_diff.json'), 'r') as fp:
                summary = json.load(fp)
            for size in ['16', '8', '1']:
                summ = summary.get(size)
                if summ:
                    hit = summ['hit']
                    miss = summ['miss']
                    total = hit + miss
                    success = hit * 100 / total
                    if size == '16':
                        mt_total_miss += miss
                        mt_total_hits += hit

                else:
                    success = 100
                report[int(size)] = f'{success:.2f} %'
            game_row = [
                f':ref:`{tag}`',
                report[16],
                report[8],
                report[1],
            ]
            data_list.append(game_row)
            

    writer = ptw.RstGridTableWriter(
        table_name="Result Sumary",
        headers=["Game", "Metatiles", "Sprites", "Pixels"],
        value_matrix=data_list,
    )

    with open(gamelist_rst, 'w') as fp:
        fp.write('Game List\n')
        fp.write('=========\n')
        fp.write('\n')
        fp.write(writer.dumps())


if __name__ == "__main__":
    main()