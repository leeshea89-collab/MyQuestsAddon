-- stock: keep items in stock in your ME network by requesting crafts automatically.
-- Setup: Adapter touching an ME Controller or ME Interface. Patterns for the items must exist.
-- Usage: stock            (uses /home/stock.cfg, created on first run)
-- stock.cfg format, one line per item:   <item name> <damage> <amount>
--   e.g.  gregtech:gt.metaitem.01 11305 256      (Steel plates)
local component = require("component")
local event = require("event")
local filesystem = require("filesystem")

local me = component.isAvailable("me_controller") and component.me_controller
        or component.isAvailable("me_interface") and component.me_interface
if not me then io.stderr:write("Put an Adapter against an ME Controller or ME Interface.\n"); return 1 end

local cfgPath = "/home/stock.cfg"
if not filesystem.exists(cfgPath) then
  local f = io.open(cfgPath, "w")
  f:write("# <item name> <damage> <amount>\nminecraft:torch 0 64\n")
  f:close()
  print("Created " .. cfgPath .. " - edit it with: edit " .. cfgPath)
end

local wanted = {}
for line in io.lines(cfgPath) do
  local name, dmg, amt = line:match("^%s*([^#%s]+)%s+(%d+)%s+(%d+)")
  if name then wanted[#wanted + 1] = {name = name, damage = tonumber(dmg), amount = tonumber(amt)} end
end
print(#wanted .. " items to keep in stock. Press any key to stop.")

local jobs = {}
while true do
  for i, w in ipairs(wanted) do
    local items = me.getItemsInNetwork({name = w.name, damage = w.damage})
    local have = items[1] and items[1].size or 0
    local job = jobs[i]
    if job and (job.isDone() or job.isCanceled()) then jobs[i] = nil; job = nil end
    if have < w.amount and not job then
      local craft = me.getCraftables({name = w.name, damage = w.damage})[1]
      if craft then
        local label = craft.getStack().label
        jobs[i] = craft.request(w.amount - have)
        print(string.format("Requested %d x %s (have %d)", w.amount - have, label, have))
      end
    end
  end
  if event.pull(10, "key_down") then break end
end
