# from unittest import TestCase
# from unittest.mock import patch
# from os.path import abspath, dirname, exists, join
# from tyler.import_image import (load_image as original_load_image,
#                                             create_metatiles as original_create_metatiles,
#                                             import_image)

# from tyler.import_image import Nametable


# here = abspath(dirname(__file__))
# BLACK = 13


# class CastlevaniaTest(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.filepath = None
#         cls.screen = None
#         cls.w = None
#         cls.h = None
#         cls.load_image_patched = patch('nes_tool.commands.import_image.load_image',
#                                        wraps=cls.load_image)
#         cls.load_image_patched.start()
#         cls.create_metatiles_patched = patch('nes_tool.commands.import_image.create_metatiles',
#                                              wraps=cls.create_metatiles)
#         cls.create_metatiles_patched.start()

#     @classmethod
#     def tearDownClass(cls):
#         cls.load_image_patched.stop()
#         cls.create_metatiles_patched.stop()

#     @classmethod
#     def load_image(cls, file):
#         if not cls.screen:
#             cls.w, cls.h, cls.screen = original_load_image(file)
#         return cls.w, cls.h, cls.screen

#     @classmethod
#     def create_metatiles(cls, w, h, screen):
#         cls.meta_tiles = original_create_metatiles(w, h, screen)
#         return cls.meta_tiles

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def given_castlevania_png(self):
#         if not self.filepath:
#             path = abspath(join(here, '..', '..', 'assets', 'screens'))
#             filename = 'Castlevania_2_-_NES_-_Title.png'
#             self.filepath = join(path, filename)
#             self.assertTrue(exists(self.filepath))

#     def when_import_image(self):
#         if self.screen is None:
#             import_image(self.filepath)

#     def assert_pixel_color(self, x, y, color):
#         self.assertEqual(self.screen[y][x], color)

#     def assert_meta_tile_is_blank(self, index):
#         mtile = self.meta_tiles[index]
#         self.assertEqual(mtile.colors, [BLACK])

#     def assert_meta_file_palette(self, index, palette):
#         mtile = self.meta_tiles[index]
#         self.assertEqual(mtile.palette, palette)

#     def assert_meta_file_colors(self, index, colors):
#         mtile = self.meta_tiles[index]
#         self.assertEqual(mtile.colors, colors)

#     def assert_tile_is_single_color(self, index):
#         mtile = self.meta_tiles[index]
#         self.assertEqual(len(mtile.colors), 1)

#     def test_load_image_pixel_0_0_is_black(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_pixel_color(0, 0, BLACK)

#     def test_metatile_first_line_blank(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         for i in range(16):
#             self.assert_meta_tile_is_blank(i)

#     def test_tile_0_is_all_one_color(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_tile_is_single_color(0)

#     def test_tile_0_is_all_one_color(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_tile_is_single_color(0)

#     def test_tile_konami_logo_colors(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_meta_file_colors(21, [13, 22, 39])

#     def test_tile_konami_logo_palette(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_meta_file_colors(21, [13, 22, 39])

#     def test_tile_konami_k_colors(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_meta_file_colors(22, [13, 16, 22, 39])

#     def test_tile_konami_k_palette(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_meta_file_palette(22, [13, 16, 22, 39])

#     def test_tile_konami_o_colors(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         self.assert_meta_file_colors(23, [13, 16])

#     def test_tile_konami_format(self):
#         self.given_castlevania_png()

#         self.when_import_image()

#         mtile = self.meta_tiles[38]

#         mtile.debug()
