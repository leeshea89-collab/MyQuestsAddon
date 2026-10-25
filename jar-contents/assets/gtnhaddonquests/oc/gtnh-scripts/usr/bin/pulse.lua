-- pulse: a redstone clock. Pulses a side every N seconds.
-- Usage: pulse <side> [interval = 5] [length = 1]
local component = require("component")
local sides = require("sides")
local event = require("event")
local shell = require("shell")
local args = shell.parse(...)
local side = sides[args[1] or ""]
local interval, length = tonumber(args[2]) or 5, tonumber(args[3]) or 1
if not side or not component.isAvailable("redstone") then print("Usage: pulse <side> [interval] [length] (needs redstone I/O)"); return 1 end
local rs = component.redstone
print("Pulsing. Press any key to stop.")
while true do
  rs.setOutput(side, 15)
  if event.pull(length, "key_down") then break end
  rs.setOutput(side, 0)
  if event.pull(math.max(0.05, interval - length), "key_down") then break end
end
rs.setOutput(side, 0)
