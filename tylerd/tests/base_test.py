from unittest import TestCase
from tylerd.base import Palette
from tylerd.platform.nes import Nes
from tylerd.platform.base import PlatformManager


class PaletteTest(TestCase):

    def test_palette_equal_palette_true(self):
        c1 = Palette([12,23,32,57])
        c2 = Palette([12,23,32,57])

        assert c1 == c2

    def test_palette_equal_palette_false(self):
        c1 = Palette([12,23,32,57])
        c2 = Palette([12,23,32,56])

        assert c1 != c2

    def test_palette_equal_using_list(self):
        c1 = Palette([12,23,32,57])
        c2 = [12, 23, 32, 57]

        assert c1 == c2

    def test_palette_equal_using_tuple(self):
        c1 = Palette([12,23,32,57])
        c2 = [12, 23, 32, 57]

        assert c1 == c2


    def test_palette_equal_using_tuple(self):
        c1 = Palette([12,23,32,57])
        c2 = [12, 23, 32, 57]

        assert c1 == c2

    def test_palette_has(self):
        c1 = Palette([12,23,32,57])
        c2 = [12, 23, 32]

        assert c1.has(c2)

    def test_palette_has_witn_one(self):
        c1 = Palette([12,23,32,57])
        c2 = [12]

        assert c1.has(c2)

    def test_palette_contains(self):
        c1 = Palette([12, 23, 32, 44])
        c2 = [12, 23, 34]

        assert c1.contains(c2) == [12, 23]


    def test_palette_not_contains(self):
        c1 = Palette([12, 23, 32, 44])
        c2 = [12, 23, 34]

        assert c1.not_contains(c2) == [34]
