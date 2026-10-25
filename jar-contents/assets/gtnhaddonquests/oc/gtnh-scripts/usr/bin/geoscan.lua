-- geoscan: find likely ore around a Geolyzer by block hardness.
-- Setup: computer with a Geolyzer next to it (or a robot/tablet with a geolyzer upgrade).
-- Usage: geoscan [radius = 8] [min hardness = 2.5]
--   Prints columns with dense blocks (ores are harder than stone: stone 1.5, most ores 3+).
local component = require("component")
local shell = require("shell")
if not component.isAvailable("geolyzer") then io.stderr:write("No geolyzer found.\n"); return 1 end
local geo = component.geolyzer
local args = shell.parse(...)
local r = math.min(tonumber(args[1]) or 8, 32)
local min = tonumber(args[2]) or 2.5
local hits = 0
print("x/z offsets from the geolyzer; y is relative height. Scanning...")
for x = -r, r do
  for z = -r, r do
    local col = geo.scan(x, z)
    for i = 1, #col do
      if col[i] >= min and col[i] < 50 then  -- >= 50 is bedrock/unbreakable
        hits = hits + 1
        print(string.format("x=%3d z=%3d y=%3d hardness=%.1f", x, z, i - 33, col[i]))
      end
    end
  end
end
print(hits .. " dense blocks found. Readings are noisy further from the geolyzer.")
