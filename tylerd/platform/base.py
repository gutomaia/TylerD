from abc import ABCMeta, abstractmethod


class Platform(metaclass=ABCMeta):
    @abstractmethod
    def get_color_code(self, color):
        pass

    @abstractmethod
    def has_metatiles(self):
        return True

    @property
    def uses_metatiles(self):
        return self.has_metatiles()

    @abstractmethod
    def get_tile_size(self):
        pass

    @property
    def tile_size(self):
        return self.get_tile_size()

    @abstractmethod
    def get_amount_colors_per_palette(self):
        pass

    @property
    def palette_slots(self):
        return self.get_amount_colors_per_palette()

    @abstractmethod
    def get_amount_background_palettes(self):
        pass

    @abstractmethod
    def get_amount_sprite_palettes(self):
        pass

    def get_width_height_screen(self, image):
        width, height = image.size
        rgb_im = image.convert('RGB')

        data = []
        assert width % self.tile_size == 0
        assert height % self.tile_size == 0
        screen = [[x for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                color_index = self.get_color_code(rgb_im.getpixel((x, y)))
                data.append(color_index)
                screen[y][x] = color_index

        return width, height, screen
    
    @abstractmethod
    def color_code_to_rgb(self, code):
        pass

    @abstractmethod
    def debug_screen(self, screen):
        pass


class PlatformManager(Platform):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.platform = None  # Initialize platform attribute
        return cls._instance
    
    def set_platform(self, platform: Platform):
        self.platform = platform

    def get_color_code(self, color):
        return self.platform.get_color_code(color)

    def has_metatiles(self):
        return self.platform.has_metatiles()

    def get_tile_size(self):
        return self.platform.get_tile_size()

    def get_amount_colors_per_palette(self):
        return self.platform.get_amount_colors_per_palette()

    def get_amount_background_palettes(self):
        return self.platform.get_amount_background_palettes()

    def get_amount_sprite_palettes(self):
        return self.platform.get_amount_sprite_palettes()

    def color_code_to_rgb(self, code):
        return self.platform.color_code_to_rgb(code)

    def debug_screen(self, screen):
        return self.platform.debug_screen(screen)