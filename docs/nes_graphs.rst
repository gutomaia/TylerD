NES Graphics Overview
=====================

Introduction
---------------------

The Nintendo Entertainment System (NES) uses a specific graphics architecture to render images on the screen. This section provides an overview of key concepts such as nametable, attribute table, sprites, and palette used in NES graphics.

Nametable
---------------------

The nametable is a memory region in the NES that stores the arrangement of background tiles for a particular screen. The NES can have up to two nametables, allowing for scrolling and seamless transitions between screens. Each tile in the nametable corresponds to a specific position on the screen and contains an index pointing to a tile in the pattern table.

Attribute Table
---------------------

The attribute table is another memory region in the NES that stores attribute information for groups of tiles in the nametable. It defines properties such as palette selection, horizontal and vertical flipping, and priority. By grouping tiles together and assigning attributes to them, developers can efficiently control the appearance of large areas of the screen.

Attributes are defined for 2x2 groups of tiles, resulting in a total of four attributes per group. Each attribute byte controls the palette selection for the corresponding 2x2 tile block. By setting the palette bits in the attribute byte, developers can specify which of the four available palettes to use for rendering the tiles in the group.

Sprites
---------------------

Sprites are individual graphic objects that can be moved independently on the screen. The NES supports up to 64 sprites, each with a size of 8x8 pixels or 8x16 pixels. Sprites are used to represent characters, enemies, projectiles, and other interactive elements in the game. They are stored in the sprite attribute table (OAM) and can be manipulated dynamically during gameplay.

Each sprite in the OAM contains information such as its position (X and Y coordinates), tile index (which tile from the pattern table to use), attributes (palette selection, horizontal and vertical flipping), and priority (determines whether the sprite appears in front of or behind background tiles). During each frame, the NES scans the OAM and renders sprites on top of the background tiles according to their attributes and priorities.

Palette
---------------------

The palette is a collection of colors used to render graphics on the NES. The NES supports a total of 64 colors, arranged in four palettes of 16 colors each. Each palette consists of three primary colors (red, green, and blue) and one transparent color. By selecting different palettes, developers can achieve a wide range of visual effects and create vibrant, detailed graphics.

Conclusion
---------------------

Understanding the concepts of nametable, attribute table, sprites, and palette is essential for developing games and applications for the NES. By mastering these concepts, developers can create engaging and visually appealing experiences for players on the iconic 8-bit console.
