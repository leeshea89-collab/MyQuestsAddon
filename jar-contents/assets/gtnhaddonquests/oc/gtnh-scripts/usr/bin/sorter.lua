-- sorter: move items from one inventory to others using a Transposer and name rules.
-- Setup: Transposer touching the input chest and the output chests.
-- Usage: sorter <inputSide> <defaultSide> [pattern=side ...]
--   e.g. sorter top bottom ore=north dust=south ingot=east
--   Patterns are Lua patterns matched against the item name (e.g. "gt.blockores").
local component = require("component")
local sides = require("sides")
local event = require("event")
local shell = require("shell")
if not component.isAvailable("transposer") then io.stderr:write("No transposer found.\n"); return 1 end
local t = component.transposer
local args = shell.parse(...)
local input, default = sides[args[1] or ""], sides[args[2] or ""]
if not input or not default then print("Usage: sorter <inputSide> <defaultSide> [pattern=side ...]"); return 1 end
local rules = {}
for i = 3, #args do
  local pat, s = args[i]:match("^(.-)=(%a+)$")
  if pat and sides[s] then rules[#rules + 1] = {pat = pat, side = sides[s]} end
end
print(#rules .. " rules. Press any key to stop.")
while true do
  local size = t.getInventorySize(input) or 0
  for slot = 1, size do
    local st = t.getStackInSlot(input, slot)
    if st then
      local target = default
      for _, r in ipairs(rules) do
        if st.name:find(r.pat) or (st.label and st.label:lower():find(r.pat)) then target = r.side break end
      end
      t.transferItem(input, target, st.size, slot)
    end
  end
  if event.pull(1, "key_down") then break end
end
