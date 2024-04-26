from abc import ABCMeta, abstractmethod
from collections import Counter
from tylerd.core.palette import Palette


class PaletteStrategy(metaclass=ABCMeta):

    @abstractmethod
    def is_applicable(self, palettes) -> bool:
        pass

    @abstractmethod
    def apply(self, nametable, palettes) -> None:
        pass

    def filter_more_relevant_palettes(self, palettes):
        relevant = sorted(palettes, key=lambda x: x.weight, reverse=True)
        return relevant[:4]
    
    def apply_palette(self, nametable, palettes):
        if isinstance(palettes, Palette):
            palettes = [palettes]
        for mt in nametable.meta_tiles:
            if mt.palette is None:
                for p in palettes:
                    if p.has(mt.colors):
                        mt.palette = p
                        break

    def create_new_palette(self, nametable, colors):
        colors = self.remove_colors_subsets(colors)
        color = colors[0]
        palette = Palette(colors[0])
        
        for color in colors[1:]:
            miss = palette.not_contains(color)
            for c in miss:
                if palette.can_add_color:
                    palette.add_color(c)

        return palette

    def fit_palette(self, nametable, palettes, fit):
        for mt in nametable.meta_tiles:
            if mt.palette is None:
                for p in palettes:
                    contains = p.contains(mt.colors)
                    if len(contains) == fit:
                        mt.palette = p
                        break

    def remove_colors_subsets(self, colors):
        colors.sort(key=len)
        set_list = [set(t) for t in colors]
        for i in range(len(set_list)):
            if set_list[i] is None:
                continue
            for j in range(i+1, len(set_list)):
                if set_list[i].issubset(set_list[j]):
                    set_list[i] = None
                    break
        set_list = [s for s in set_list if s is not None]
        return [tuple(s) for s in set_list]

    def rearrange_colors(self, colors):
        # Sort the subset list by length of subsets in descending order
        colors.sort(key=len, reverse=True)
        
        # Initialize a dictionary to store the result
        result = {}
        
        # Define a recursive function to group subsets
        def group_subsets(subsets, current_group):
            if not subsets:
                result[len(result)] = current_group[:]
                return
            subset = subsets.pop()
            for group in current_group:
                if not (subset & group):
                    group_subsets(subsets[:], current_group + [subset & group])
                    break
            else:
                group_subsets(subsets[:], current_group + [subset])
            group_subsets(subsets[:], current_group)
        
        # Initialize the recursive function
        group_subsets(colors[:], [])
        
        # Get the result with the fewest sets
        min_sets = min(result.values(), key=len)
        
        return min_sets




class HasFourMainPalettes(PaletteStrategy):

    def is_applicable(self, palettes) -> bool:
        return len(palettes) == 4
    
    def apply(self, nametable, palettes):
        nametable.tile_palettes = palettes
        self.apply_palette(nametable, palettes)


        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if colors:
            for c in colors:
                for p in palettes:
                    contains = p.contains(c)
                    if len(contains) == 4:
                        for mt in unmatched_mt:
                            if mt.colors == c:
                                mt.palette = p
                        break
            unmatched_mt = [
                mt
                for mt in nametable.meta_tiles
                if mt.palette is None
            ]

        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if colors:
            for mt in unmatched_mt:
                mt.palette = palettes[0]

        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        if len(unmatched_mt) > 0:
            raise Exception('misses palettes')


class HasLessThenFourMainPalettes(PaletteStrategy):

    def is_applicable(self, palettes) -> bool:
        return len(palettes) < 4
    
    def apply(self, nametable, palettes):
        nametable.tile_palettes = palettes
        self.apply_palette(nametable, palettes)
        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None and len(mt.colors) <= 4
        ]
        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if colors:
            palette = self.create_new_palette(nametable, colors)
            nametable.tile_palettes.append(palette)
            self.apply_palette(nametable, palette)

        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if colors:
            for c in colors:
                for p in palettes:
                    contains = p.contains(c)
                    if len(contains) == 4:
                        palette = Palette(contains)
                        nametable.tile_palettes.append(palette)
                        for mt in unmatched_mt:
                            if mt.colors == c:
                                mt.palette = palette
                        break
        
        colors = self.remove_colors_subsets(colors)
        # colors = self.rearrange_colors(colors)
        if len(palettes) + len(colors) <= 4:
            for c in colors:
                p = Palette(c)
                nametable.tile_palettes.append(p)

        self.fit_palette(nametable, palettes, 3)
        self.fit_palette(nametable, palettes, 2)
        self.fit_palette(nametable, palettes, 1)

        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]
        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if len(unmatched_mt) > 0:
            raise Exception('misses palettes')


        # if unmatched_mt:
        #     unmatched_colors = dict(
        #         Counter([mt.colors for mt in unmatched_mt])
        #     )
        #     unmatched = [
        #         [v, 0, k] for k, v in unmatched_colors.items()
        #     ]   # counter, fill, dict
        #     unmatched.sort(key=lambda s: s[0], reverse=True)

        #     new_colors = {}
        #     for index, u1 in enumerate(unmatched):
        #         for u2 in unmatched:
        #             if u1[2] == u2[2]:
        #                 continue
        #             elif all([u in u1[2] for u in u2[2]]):
        #                 unmatched[index][0] += u2[0]
        #             new_color = list(set(u1[2] + u2[2]))
        #             new_color.sort()
        #             new_color = tuple(new_color)
        #             if (
        #                 len(new_color) <= 4
        #                 and new_color not in unmatched_colors.keys()
        #                 and not new_color in new_colors.keys()
        #             ):
        #                 new_colors[new_color] = 0

        #     for count, fill, color in unmatched:
        #         for k, v in new_colors.items():
        #             if all([c in k for c in color]):
        #                 new_colors[k] += count

        #     unmatched.extend([[v, 0, k] for k, v in new_colors.items()])
        #     unmatched.sort(key=lambda s: (s[0], s[1]), reverse=True)

        #     print('unmatched', unmatched)

        #     print(self.tile_palettes)
        #     while len(self.tile_palettes) != 4 and len(unmatched) > 0:
        #         _, _, palette = unmatched.pop(0)
        #         print(unmatched)
        #         print(palette)
        #         if len(self.tile_palettes) == 0:
        #             self.tile_palettes.append(palette)
        #             print('added palette', palette)
        #         else:
        #             for p1 in self.tile_palettes:
        #                 print('loop', p1, ([p2 in p1 for p2 in palette]))
        #                 if not all([p2 in p1 for p2 in palette]):
        #                     self.tile_palettes.append(palette)

        #     print(self.tile_palettes)

        #     # import pdb; pdb.set_trace()
        #     # raise Exception('Im here')
        #     matches = {}

class HasMoreThenFourMainPalettes(PaletteStrategy):

    def is_applicable(self, palettes) -> bool:
        return len(palettes) > 4
   
    def apply(self, nametable, palettes) -> None:
        relevant = self.filter_more_relevant_palettes(palettes)
        nametable.tile_palettes = relevant

        self.apply_palette(nametable, relevant)

        self.fit_palette(nametable, relevant, 3)                     
        self.fit_palette(nametable, relevant, 2)                     
        self.fit_palette(nametable, relevant, 1)
        
        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        unmatched_colors = [mt.colors for mt in unmatched_mt]
        scores = Counter(unmatched_colors)
        colors = [c for c,_ in scores.most_common()]

        if colors:
            for mt in unmatched_mt:
                mt.palette = relevant[0]

        unmatched_mt = [
            mt
            for mt in nametable.meta_tiles
            if mt.palette is None
        ]

        if len(unmatched_mt) > 0:
            raise Exception('misses palettes')
