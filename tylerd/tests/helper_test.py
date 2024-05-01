from unittest import TestCase
from tylerd.helper import str_bytes, hex_to_rgb, get_metatile


class HelperTest(TestCase):
    def test_str_bytes(self):
        actual = str_bytes([0x30, 0x1C, 0x0C, 0x0E])
        self.assertEqual(actual, ' .byte $30, $1c, $0c, $0e\n')

    def test_str_bytes_counting(self):
        actual = str_bytes([1, 2, 3, 4])
        self.assertEqual(actual, ' .byte $01, $02, $03, $04\n')

    def test_str_bytes_arrange_2(self):
        actual = str_bytes([1, 2, 3, 4], arrange=2)
        self.assertEqual(actual, ' .byte $01, $02\n .byte $03, $04\n')

    def test_hex_to_rgb(self):
        actual = hex_to_rgb(0xC8C0C0)
        self.assertEqual(actual, (0xC8, 0xC0, 0xC0))

    def test_hex_to_rgb_2(self):
        actual = hex_to_rgb(0x010203)
        self.assertEqual(actual, (0x01, 0x02, 0x03))

    # def test_get_color_index_black(self):
    #     actual = get_color_index((0, 0, 0))
    #     self.assertEqual(actual, 13)

    # def test_get_color_index_red(self):
    #     actual = get_color_index((255, 0, 0))
    #     self.assertEqual(actual, 22)

    # def test_get_color_index_green(self):
    #     actual = get_color_index((0, 255, 0))
    #     self.assertEqual(actual, 26)

    # def test_get_color_index_blue(self):
    #     actual = get_color_index((0, 0, 255))
    #     self.assertEqual(actual, 18)

    def test_get_metatile_0(self):
        data = [[0] * 16] * 16
        actual = get_metatile(data, 0, 0)
        self.assertEqual(actual, [0] * 16 * 16)

    def test_get_metatile_1(self):
        data = [([0] * 16) + ([1] * 16)] * 16
        actual = get_metatile(data, 1, 0)
        self.assertEqual(actual, [1] * 16 * 16)

    def test_get_metatile_2(self):
        data = ([([0] * 16) + ([1] * 16)] * 16) + (
            [([2] * 16) + ([3] * 16)] * 16
        )
        actual = get_metatile(data, 0, 1)
        self.assertEqual(actual, [2] * 16 * 16)

    def test_get_metatile_3(self):
        data = ([([0] * 16) + ([1] * 16)] * 16) + (
            [([2] * 16) + ([3] * 16)] * 16
        )
        actual = get_metatile(data, 1, 1)
        self.assertEqual(actual, [3] * 16 * 16)
