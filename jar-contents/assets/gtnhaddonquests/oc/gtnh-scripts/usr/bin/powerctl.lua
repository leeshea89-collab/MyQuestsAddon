-- powerctl: switch generators on/off with redstone to keep a GT energy store between two limits.
-- Setup: Adapter on the battery buffer/LSC, Redstone I/O block (or redstone card) wired to your generators.
-- Usage: powerctl <side> [low% = 30] [high% = 90]
--   Redstone ON at <side> when charge drops below low%, OFF once it passes high%.
--   side: bottom, top, north, south, west, east
local component = require("component")
local sides = require("sides")
local event = require("event")
local shell = require("shell")

local args = shell.parse(...)
local side = sides[args[1] or ""]
local low, high = tonumber(args[2]) or 30, tonumber(args[3]) or 90
if not side then
  print("Usage: powerctl <side> [low%] [high%]")
  return 1
end
if not component.isAvailable("redstone") then
  io.stderr:write("Needs a Redstone I/O block or redstone card.\n"); return 1
end
local rs = component.redstone
local dev
for addr, name in component.list() do
  if name == "LSC" or name == "gt_energyContainer" then dev = component.proxy(addr) break end
end
if not dev then io.stderr:write("No GregTech energy block on an Adapter.\n"); return 1 end

local on = false
print(string.format("Keeping charge between %d%% and %d%%. Press any key to stop.", low, high))
while true do
  local pct = dev.getStoredEU() / math.max(1, dev.getEUCapacity()) * 100
  if not on and pct < low then on = true elseif on and pct > high then on = false end
  rs.setOutput(side, on and 15 or 0)
  io.write(string.format("\rCharge %5.1f%%  generators %s   ", pct, on and "ON " or "OFF"))
  if event.pull(2, "key_down") then break end
end
rs.setOutput(side, 0)
print("\nStopped; redstone off.")
