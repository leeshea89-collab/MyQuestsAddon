-- lscalarm: warn the server chat (Computronics Chat Box) when your LSC or battery buffer runs low.
-- Setup: Adapter on the LSC/battery buffer, Chat Box connected to the computer.
-- Usage: lscalarm [warn% = 20]
local component = require("component")
local event = require("event")
local shell = require("shell")
local args = shell.parse(...)
local warn = tonumber(args[1]) or 20
local dev
for addr, name in component.list() do
  if name == "LSC" or name == "gt_energyContainer" then dev = component.proxy(addr) break end
end
if not dev then io.stderr:write("No GregTech energy block on an Adapter.\n"); return 1 end
local chat = component.isAvailable("chat_box") and component.chat_box
if chat and chat.setName then chat.setName("Power") end
local alerted = false
print("Watching charge. Press any key to stop.")
while true do
  local pct = dev.getStoredEU() / math.max(1, dev.getEUCapacity()) * 100
  if pct < warn and not alerted then
    local msg = string.format("Warning: base power at %.1f%%!", pct)
    if chat then chat.say(msg) else print(msg) end
    alerted = true
  elseif pct > warn + 10 then
    alerted = false
  end
  if event.pull(5, "key_down") then break end
end
