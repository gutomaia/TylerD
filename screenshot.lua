print('Script started')
emu.speedmode('maximum');
local filename
repeat
    filename = rom.getfilename();
    emu.frameadvance();
until filename ~= nil;
-- local name = filename:match("(.*)%..*")
local name = filename
local screenshot = string.format("output/%s_screenshot.png", name)
for i=1,100 do emu.frameadvance();
end; 
gui.savescreenshotas(screenshot);
emu.frameadvance();
emu.exit();
