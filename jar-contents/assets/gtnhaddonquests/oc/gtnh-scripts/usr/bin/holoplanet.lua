-- holoplanet: draw a ringed planet with a Hologram Projector.
-- Usage: holoplanet [radius = 10]
local component = require("component")
local shell = require("shell")
if not component.isAvailable("hologram") then io.stderr:write("No hologram projector found.\n"); return 1 end
local h = component.hologram
local args = shell.parse(...)
local R = math.min(tonumber(args[1]) or 10, 14)
h.clear()
pcall(h.setPaletteColor, 1, 0x3366CC)  -- planet (tier 2 projectors have 3 colours)
pcall(h.setPaletteColor, 2, 0xCC9944)  -- ring
pcall(h.setPaletteColor, 3, 0xFFFFFF)  -- ice cap
local cx, cy, cz = 24, 16, 24
for x = cx - R, cx + R do
  for z = cz - R, cz + R do
    for y = cy - R, cy + R do
      local d = (x - cx) ^ 2 + (y - cy) ^ 2 + (z - cz) ^ 2
      if d <= R * R and d > (R - 1.5) ^ 2 then
        h.set(x, y, z, (y - cy) > R * 0.75 and 3 or 1)
      end
    end
  end
end
for a = 0, 359, 2 do
  for rr = R + 3, R + 6 do
    local x = math.floor(cx + rr * math.cos(math.rad(a)) + 0.5)
    local z = math.floor(cz + rr * math.sin(math.rad(a)) + 0.5)
    if x >= 1 and x <= 48 and z >= 1 and z <= 48 then h.set(x, cy, z, 2) end
  end
end
print("Planet drawn. Use 'holoplanet' again with a new radius, or hologram.clear() to wipe.")
