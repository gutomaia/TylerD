#include "neslib.h"

// #link "output/{{name}}_tiles.s"
extern const byte {{name}}_chr[];
extern const byte {{name}}_pal[];
extern const byte {{name}}_nam[];
extern const byte {{name}}_attr[];


void put_256inc() {
  word i;
  for (i=0; i<256; i++)
    vram_put(0xff);
}

void put_attrib() {
  vram_adr(NAMETABLE_A + 0x3c0);
  vram_fill(0x00, 0x0f);
}

void clear() {
  vram_adr(0x0);
  vram_fill(0x0, 0x2000);
}

void erase_board()
{
  clear();
  vram_adr(NAMETABLE_A);
  put_256inc();
  put_256inc();
  put_256inc();
  put_256inc();
  put_attrib();
}

void fade_in() {
  byte vb;
  for (vb=0; vb<=4; vb++) {
    // set virtual bright value
    pal_bright(vb);
    // wait for 4/60 sec
    ppu_wait_frame();
    ppu_wait_frame();
    ppu_wait_frame();
    ppu_wait_frame();
  }
}

void render_screen(const byte* pal, const byte* chr, const byte* nam, const byte* attr) {
  // disable rendering
  ppu_off();
  // set palette, virtual bright to 0 (total black)
  pal_bg(pal);
  pal_bright(0);

  // unpack nametable into the VRAM
  bank_bg(0);
  vram_adr(0x0000);
  vram_write(chr, 255*16);

  vram_adr (NAMETABLE_B);
  vram_write(nam, 880);

  vram_adr (NAMETABLE_B + 0x3C0);
  vram_write(attr, 224);

  ppu_on_all();
  fade_in();
}

void main(void)
{
  erase_board();
  render_screen({{name}}_pal, {{name}}_chr, {{name}}_nam, {{name}}_attr);

  while(1);//do nothing, infinite loop
}
