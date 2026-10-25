-- power: live monitor for a GregTech battery buffer, machine or Lapotronic Supercapacitor.
-- Setup: computer + screen + Adapter touching the GT block (or the LSC controller).
-- Usage: power [refresh-seconds]    (Ctrl+C or any key to quit)
local component = require("component")
local term = require("term")
local event = require("event")
local shell = require("shell")

local args = shell.parse(...)
local refresh = tonumber(args[1]) or 1

local function find()
  for addr, name in component.list() do
    if name == "LSC" then return component.proxy(addr), "Lapotronic Supercapacitor" end
  end
  for addr, name in component.list() do
    if name == "gt_energyContainer" then return component.proxy(addr), "GregTech energy block" end
  end
end

local dev, kind = find()
if not dev then
  io.stderr:write("No GregTech energy block found. Place an Adapter against a battery buffer, machine or LSC.\n")
  return 1
end

local function si(n)
  local units = {"", "k", "M", "G", "T", "P", "E"}
  local i = 1
  while math.abs(n) >= 1000 and i < #units do n = n / 1000; i = i + 1 end
  return string.format("%.2f%s", n, units[i])
end

local gpu = component.gpu
local w = gpu.getResolution()
local last
while true do
  local stored, cap = dev.getStoredEU(), dev.getEUCapacity()
  local pct = cap > 0 and stored / cap or 0
  term.clear()
  print(kind)
  print(string.rep("=", #kind))
  print(string.format("Stored : %s / %s EU (%.1f%%)", si(stored), si(cap), pct * 100))
  if dev.getAverageElectricInput then
    print(string.format("In/Out : %s / %s EU/t (avg)", si(dev.getAverageElectricInput()), si(dev.getAverageElectricOutput())))
  end
  if last then
    local rate = (stored - last) / (refresh * 20)
    print(string.format("Change : %s EU/t", si(rate)))
  end
  last = stored
  local bar = math.max(10, w - 2)
  local filled = math.floor(bar * pct + 0.5)
  print("[" .. string.rep("#", filled) .. string.rep(".", bar - filled) .. "]")
  print("\nPress any key to exit.")
  if event.pull(refresh, "key_down") then break end
end
term.clear()
