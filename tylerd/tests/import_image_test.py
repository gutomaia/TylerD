# from unittest import TestCase
# from tyler.commands.import_image import Tile, MetaTile

# R = 22
# G = 25
# B = 1


# class TileTest(TestCase):

#     def test_tile(self):
#         data = [R] * 8 * 8
#         data[0] = 10
#         t = Tile(data)
#         self.assertEqual(10, t.get(0, 0))

#     def test_tile_1(self):
#         data = [R] * 8 * 8
#         data[8] = 10
#         t = Tile(data)
#         self.assertEqual(10, t.get(0, 1))


# class MetaTileTest(TestCase):

#     def test_metatile(self):
#         data = ([R] * 8 + [G] * 8) * 8 + ([B] * 8 + [R] * 8) * 8
#         mt = MetaTile(data)

#         self.assertEqual(mt.tiles[0].data, [R] * 8 * 8)
#         self.assertEqual(mt.tiles[1].data, [G] * 8 * 8)
#         self.assertEqual(mt.tiles[2].data, [B] * 8 * 8)
#         self.assertEqual(mt.tiles[3].data, [R] * 8 * 8)

#     def test_metatile_colors(self):
#         data = ([R] * 8 + [G] * 8) * 8 + ([B] * 8 + [R] * 8) * 8
#         mt = MetaTile(data)

#         self.assertIn(R, mt.colors)
#         self.assertIn(G, mt.colors)
#         self.assertIn(B, mt.colors)

#     def test_metatile_color_without_blue(self):
#         data = ([R] * 8 + [G] * 8) * 8 + ([G] * 8 + [R] * 8) * 8
#         mt = MetaTile(data)

#         self.assertIn(R, mt.colors)
#         self.assertIn(G, mt.colors)
#         self.assertNotIn(B, mt.colors)

#     def test_metatile_palette_after_fix_palette(self):
#         data = ([R] * 8 + [G] * 8) * 8 + ([B] * 8 + [R] * 8) * 8
#         mt = MetaTile(data)
