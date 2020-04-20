# Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py
# ===========================================
#
# You can use an Oculus Go VR headseat to play Half-Life: Alyx on your PC.
# You will need to install some free software, including ALVR and FreePIE.
# This FreePIE script allows / help you play the game by binding specific
# game actions to the Oculus Go controller and your PC keyboard.
# Optionally, you can use a Gear VR controller instead of the keyboard.
# More details at https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go
#
# 2020.04.18 - Added support for the Gear VR (and maybe Daydream?) controller with FreePIEVRController;
#              Download DLL plugin at https://github.com/polygraphene/FreePIEVRController/releases
# 2020.04.02 - 2nd release, flick of the wrist solved with new driver; 
#              reduced flight speed for better aiming, use single controller by default.
# 2020.03.27 - [WIP] 1st release, still can't trigger a flick of the wrist

# Based on sample3.py from https://github.com/polygraphene/ALVR/wiki/FreePIE-Integration
# References:
# https://github.com/polygraphene/ALVR/wiki/FreePIE-Reference
# https://github.com/AndersMalmgren/FreePIE/wiki/Reference

# This script provides the following mappings & functions:
#     [Go trigger button]............: "trigger" (shoot, catch, hold, ...)
#     [Go trackpad click]............: "trackpad_click" (select weapon, teleport, game menu, ...)
#     [Go back button], [X]..........: "application_menu" (reload, arm grenade, ...)
#     [Space], [Gear VR trigger].....: toggle mode between "default" and "fly", and reset head & hand positions
#	  [Gear VR back].................: reset head & hand positions
#     [Alt], [Gear VR touchpad click]: faster flying speed
#     [Left-Ctrl]....................: swap controller [left / right] (currently disabled)

# Mode 0: default / passtrough
#     In default mode, use the Go trackpad as instructed by the game.
#
# Mode 1: fly
#     In fly mode, point the Go controller to the direction you want to fly.
#     Click and hold the upper part of the Go trackpad to fly forward.
#     Click and hold the lower part of the Go trackpad to fly backwards.
#     Hold [Space] or the [Gear VR trigger] to fly both your head and hand,
#     or else only your hand will move.
#     Changing mode again will reset your head and hand positions.
#
# Mode 2: trackpad guesture mode (currently disabled)
#     trackpad-left click : "application_menu" 
#     trackpad-right click: "system" 
#     trackpad-down click : "grip" 

# Vive controller image: https://forums.unrealengine.com/filedata/fetch?id=1111783&d=1460020388
# Vive controller button mappings to keyboard, Oculus Go controller and Gear VR controller:
#     "application_menu": [X],  (mode 2) [Go trackpad-left click] OR [Go back button] (in any mode)
#     "system"..........: [G],  (mode 2) [Go trackpad-right click]
#     "grip"............: [F1], (mode 2) [Go trackpad-down click]
#     "trigger".........: [T],  [Go trigger]
#     "trackpad_click"..: [F2], [Go trackpad click]
#     "back"............: [F3]
#     "guide"...........: [F4]
#     "start"...........: [F5]
#     "dpad_left".......: [F6]
#     "dpad_up".........: [F7]
#     "dpad_right"......: [F8]
#     "dpad_down".......: [F9]
#     "trackpad_touch"..: [F10]
#     "a"...............: [V]
#     "b"...............: [B]
#     "x"...............: [N]
#     "y"...............: [M]

import math, time

global prev_back, mode, offset, message_time

# Global variables / Configuration

BACK_BUTTON_BINDING   = "application_menu" # "grip"
alvr.two_controllers  = not True
flight_speed          = 0.001
speed_multiplier      = 10
mode_toggle_key       = Key.Space # Key.Tab
speed_toggle_key      = Key.LeftAlt
controller_toggle_key = Key.LeftControl
key_map = [["system", Key.G], ["application_menu", Key.X], ["trigger", Key.T], ["a", Key.V], ["b", Key.B], ["x", Key.N], ["y", Key.M]
, ["grip", Key.F1], ["trackpad_click", Key.F2], ["back", Key.F3], ["guide", Key.F4], ["start", Key.F5]
, ["dpad_left", Key.F6], ["dpad_up", Key.F7], ["dpad_right", Key.F8], ["dpad_down", Key.F9], ["trackpad_touch", Key.F10]]

# Don't change the code below if you don't know what you are doing.

def sign(x): return 1 if x >= 0 else -1

# conjugate quaternion
def conj(q):
  return [-q[0], -q[1], -q[2], q[3]]

# multiplication of quaternion
def multiply(a, b):
  x0, y0, z0, w0 = a
  x1, y1, z1, w1 = b
  return [x1 * w0 - y1 * z0 + z1 * y0 + w1 * x0,
      x1 * z0 + y1 * w0 - z1 * x0 + w1 * y0,
      -x1 * y0 + y1 * x0 + z1 * w0 + w1 * z0,
      -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0]

# convert quaternion to euler
def quaternion2euler(q):
  yaw_pitch_roll = [0.0, 0.0, 0.0]
  # roll (x-axis rotation)
  sinr = +2.0 * (q[3] * q[0] + q[1] * q[2])
  cosr = +1.0 - 2.0 * (q[0] * q[0] + q[1] * q[1])
  yaw_pitch_roll[2] = atan2(sinr, cosr)

  # pitch (y-axis rotation)
  sinp = +2.0 * (q[3] * q[1] - q[2] * q[0])
  if (fabs(sinp) >= 1):
    yaw_pitch_roll[1] = math.copysign(M_PI / 2, sinp)
  else:
    yaw_pitch_roll[1] = math.asin(sinp)

  # yaw (z-axis rotation)
  siny = +2.0 * (q[3] * q[2] + q[0] * q[1]);
  cosy = +1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]);
  yaw_pitch_roll[0] = math.atan2(siny, cosy);

  return yaw_pitch_roll

# convert euler to quaternion
def euler2quaternion(yaw_pitch_roll):
  cy = math.cos(yaw_pitch_roll[0] * 0.5);
  sy = math.sin(yaw_pitch_roll[0] * 0.5);
  cr = math.cos(yaw_pitch_roll[2] * 0.5);
  sr = math.sin(yaw_pitch_roll[2] * 0.5);
  cp = math.cos(yaw_pitch_roll[1] * 0.5);
  sp = math.sin(yaw_pitch_roll[1] * 0.5);

  return [cy * sr * cp - sy * cr * sp,
  cy * cr * sp + sy * sr * cp,
  sy * cr * cp - cy * sr * sp,
  cy * cr * cp + sy * sr * sp]

# rotate specified vector using yaw_pitch_roll
def rotatevec(yaw_pitch_roll, vec):
  q = euler2quaternion(yaw_pitch_roll)
  return multiply(multiply(q, vec), conj(q))

if starting:
  prev_back = False
  mode = 0
  modeName = ["0: default", "1: fly", "2: trackpad gesture"]
  offset  = [0.0, 0.0, 0.0]
  offset2 = [0.0, 0.0, 0.0]
  message_time = 0.0
  controller = 0
  controller_pos = [0.0, 0.0, 0.0]
  for i in range(3):
    alvr.controller_position[controller][i] = alvr.input_controller_position[i]
  gearvr = "vrcontroller" in globals()
  if not gearvr:
    diagnostics.debug("Gear VR controller plugin not found!")
    diagnostics.debug("Be sure to move the FreePIEVRController.dll file into the FreePIE plugins folder")
    diagnostics.debug('then right-click the file, select Properties and check "Unblock".')
  else:
    diagnostics.debug("Gear VR controller plugin found.")
    if not hasattr(vrcontroller[0], 'BUTTONS'):
      diagnostics.debug("Gear VR controller not found. Is Bluetooth on your computer turned on?")
      gearvr = False
  if gearvr:
    gearvr_last_trigger = False

if gearvr:
  gearvr_trigger = vrcontroller[0].trigger

# change target controller
if alvr.two_controllers and controller_toggle_key and keyboard.getPressed(controller_toggle_key):
  controller = 1 - controller
  alvr.message = "%s controller" % ("Left" if controller == 1 else "Right") 
  message_time = time.time()

for k in key_map:
  alvr.buttons[controller][alvr.Id(k[0])] = keyboard.getKeyDown(k[1])

if keyboard.getPressed(mode_toggle_key) or (gearvr and gearvr_trigger and not gearvr_last_trigger):
  mode = (mode + 1) % 2
  # show messageo on display
  alvr.message = modeName[mode]
  message_time = time.time()
  offset  = [0.0, 0.0, 0.0]
  offset2 = [0.0, 0.0, 0.0]

if time.time() - message_time > 2:
  # remove message after 2 seconds
  alvr.message = ""

# reset offsets with Gear VR back button
if gearvr and vrcontroller[0].app: 
  offset  = [0.0, 0.0, 0.0]
  offset2 = [0.0, 0.0, 0.0]

trigger_on = alvr.buttons[controller][alvr.Id("trigger")] or alvr.input_buttons[alvr.InputId("trigger")]

if mode == 2:
  # trackpad guesture mode
  alvr.buttons[controller][alvr.Id("trigger")] = trigger_on 
  #alvr.buttons[controller][alvr.Id("application_menu")] = alvr.buttons[controller][alvr.Id("application_menu")] or alvr.input_buttons[alvr.InputId("back")]

  if alvr.input_buttons[alvr.InputId("trackpad_click")]:
    if alvr.input_trackpad[0] + alvr.input_trackpad[1] > 0.0:
      if alvr.input_trackpad[0] - alvr.input_trackpad[1] > 0.0:
        # right
        alvr.buttons[controller][alvr.Id("system")] = True
      else:
        # top
        alvr.buttons[controller][alvr.Id("trackpad_click")] = True
        alvr.buttons[controller][alvr.Id("trackpad_touch")] = True
    else:
      if alvr.input_trackpad[0] - alvr.input_trackpad[1] > 0.0:
        # bottom
        alvr.buttons[controller][alvr.Id("grip")] = True
      else:
        # left
        alvr.buttons[controller][alvr.Id("application_menu")] = True
elif mode == 1:
  # fly mode
  # press upper half of trackpad to move forward. bottom half to move back
  if alvr.input_buttons[alvr.InputId("trackpad_click")]:
    #if alvr.input_buttons[alvr.InputId("trigger")] and alvr.input_trackpad[0] - alvr.input_trackpad[1] > 0.0:
    #  offset = [0.0, 0.0, 0.0]
    #else:
      outvec = rotatevec(alvr.input_controller_orientation, [0, 0, -1, 0])
      speed  = flight_speed * sign(alvr.input_trackpad[1])
      if keyboard.getKeyDown(speed_toggle_key) or (gearvr and vrcontroller[0].click):
        speed = speed * speed_multiplier
      for i in range(3):
        offset[i] += speed * outvec[i]

  alvr.buttons[controller][alvr.Id("trigger")] = trigger_on
elif mode == 0:
  # passthrough mode
  alvr.buttons[controller][alvr.Id("trackpad_click")] = alvr.buttons[controller][alvr.Id("trackpad_click")] or alvr.input_buttons[alvr.InputId("trackpad_click")]
  alvr.buttons[controller][alvr.Id("trackpad_touch")] = alvr.buttons[controller][alvr.Id("trackpad_touch")] or alvr.input_buttons[alvr.InputId("trackpad_touch")]
  alvr.buttons[controller][alvr.Id("trigger")] = trigger_on
  alvr.trackpad[controller][0] = alvr.input_trackpad[0]
  alvr.trackpad[controller][1] = alvr.input_trackpad[1]

# You need to set trigger value correctly to get trigger click work
alvr.trigger[controller] = 1.0 if alvr.buttons[controller][alvr.Id("trigger")] else 0.0

# Use Gear VR controller vol. up / down buttons to displace hand position as well, even outside of fly mode.
if gearvr and (vrcontroller[0].volup or vrcontroller[0].voldown):
  outvec = rotatevec(alvr.input_controller_orientation, [0, 0, -1, 0])
  speed  = -flight_speed if vrcontroller[0].voldown else flight_speed
  for i in range(3):
    offset2[i] += speed * outvec[i]


alvr.override_head_position          = True
alvr.override_controller_position    = True
alvr.override_controller_orientation = True
for i in range(3):
  if keyboard.getPressed(mode_toggle_key) or (gearvr and gearvr_trigger):
    alvr.head_position[i] = alvr.input_head_position[i] + offset[i] # + offset2[i] 
  #alvr.controller_position[controller][i] = alvr.input_controller_position[i] + offset[i] + offset2[i]
  alvr.controller_orientation[controller][i] = alvr.input_controller_orientation[i]

if False: #trigger_on:
  # We need to change Y and Z axes
  if False:
    hw  = 0.15 # estimated "hand width", from finger to wrist, in meters
    r   = 0.15 # estimated radius from axis used by ALVR to rotate the controller, in meters
    hhw = hw / 2.0 
    pitch = alvr.input_controller_orientation[2] # in radians. Doc says [yaw,pitch,roll], though...
    y1 = (r + hhw) * math.sin(pitch)
    z1 = (r + hhw) * math.cos(pitch)
    y2 = hhw * math.sin(pitch)
    z2 = r + hw + hhw*math.cos(pitch+math.pi)
    diagnostics.watch(pitch); diagnostics.watch(y1);diagnostics.watch(z1); diagnostics.watch(y2);diagnostics.watch(z2)   
    alvr.controller_position[controller][0] = controller_pos[0] + offset[0]
    alvr.controller_position[controller][1] = controller_pos[1] + offset[1] + y1 + y2
    alvr.controller_position[controller][2] = controller_pos[2] + offset[2] + (r+hhw -z1) + z2 
else:
  for i in range(3):
    alvr.controller_position[controller][i] = controller_pos[i] + offset[i] + offset2[i]
    controller_pos[i] = alvr.input_controller_position[i]

# Button remapping:
alvr.buttons[controller][alvr.Id(BACK_BUTTON_BINDING)] = alvr.input_buttons[alvr.InputId("back")]

if gearvr:
  gearvr_last_trigger = gearvr_trigger

if not True:
  # watch variables on FreePIE debugger
  diagnostics.watch(alvr.input_head_orientation[0]) 
  diagnostics.watch(alvr.input_head_orientation[1]) 
  diagnostics.watch(alvr.input_head_orientation[2]) 
  diagnostics.watch(alvr.input_controller_orientation[0])
  diagnostics.watch(alvr.input_controller_orientation[1])
  diagnostics.watch(alvr.input_controller_orientation[2])
  diagnostics.watch(alvr.input_head_position[0])
  diagnostics.watch(alvr.input_head_position[1])
  diagnostics.watch(alvr.input_head_position[2])
  diagnostics.watch(alvr.input_controller_position[0])
  diagnostics.watch(alvr.input_controller_position[1])
  diagnostics.watch(alvr.input_controller_position[2])
  diagnostics.watch(alvr.input_trackpad[0])
  diagnostics.watch(alvr.input_trackpad[1])
  diagnostics.watch(alvr.input_buttons[0])
  diagnostics.watch(alvr.input_buttons[1])
  diagnostics.watch(alvr.input_buttons[2])
  diagnostics.watch(alvr.input_buttons[3])
  diagnostics.watch(alvr.input_buttons[4])
  diagnostics.watch(alvr.input_buttons[5])
  diagnostics.watch(alvr.head_position[0])
  diagnostics.watch(alvr.head_position[1])
  diagnostics.watch(alvr.head_position[2])
