-- treefarm: a simple robot tree farm.
-- Setup: robot facing a dirt block, saplings in slot 1, an axe or GT saw equipped (tool slot).
-- The robot plants, waits for the tree, chops the trunk going up, then returns.
-- Usage (on the robot): treefarm [cycles = infinite]
local robot = require("robot")
local shell = require("shell")
local args = shell.parse(...)
local cycles = tonumber(args[1]) or math.huge
local function chop()
  local up = 0
  robot.swing()
  robot.forward()
  while robot.detectUp() do robot.swingUp(); robot.up(); up = up + 1 end
  for _ = 1, up do robot.down() end
  robot.back()
end
local n = 0
while n < cycles do
  robot.select(1)
  if not robot.detect() then robot.place() end
  os.sleep(30)
  local ok, what = robot.detect()
  if ok and what == "solid" then
    chop()
    n = n + 1
    print("Tree " .. n .. " chopped.")
  end
end
