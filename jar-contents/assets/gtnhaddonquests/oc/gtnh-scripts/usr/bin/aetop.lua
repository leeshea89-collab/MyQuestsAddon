-- aetop: show the most plentiful items in your ME network and its power use.
-- Setup: Adapter touching an ME Controller or ME Interface.   Usage: aetop [count = 20]
local component = require("component")
local shell = require("shell")
local args = shell.parse(...)
local count = tonumber(args[1]) or 20
local me = component.isAvailable("me_controller") and component.me_controller
        or component.isAvailable("me_interface") and component.me_interface
if not me then io.stderr:write("Put an Adapter against an ME Controller or ME Interface.\n"); return 1 end
local items = me.getItemsInNetwork()
table.sort(items, function(a, b) return a.size > b.size end)
print(string.format("%-40s %12s", "Item", "Amount"))
for i = 1, math.min(count, #items) do
  print(string.format("%-40s %12d", items[i].label:sub(1, 40), items[i].size))
end
print(string.format("\n%d item types. Power use: %.1f AE/t", #items, me.getAvgPowerUsage()))
