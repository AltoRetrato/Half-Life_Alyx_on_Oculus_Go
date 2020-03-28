# Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py
# 2020.03.27 - [WIP] 1st release, still can't trigger a flick of the wrist

# Based on sample3.py from https://github.com/polygraphene/ALVR/wiki/FreePIE-Integration
# References:
# https://github.com/polygraphene/ALVR/wiki/FreePIE-Reference
# https://github.com/AndersMalmgren/FreePIE/wiki/Reference

# [Go Back button]: "grip"
# [Left-Ctrl]..: swap controller [left / right]
# [Space]......: change mode
# Mode 0: default / passtrough
# Mode 1: fly
#     Click trackpad-up to fly forward, 
#           trackpad-down to fly backwards,
#           hold left [Alt] key to fly 10x faster.
# Mode 2: trackpad guesture mode [disabled for Half-Life: Alyx]
#     trackpad-left click : "application_menu" 
#     trackpad-right click: "system" 
#     trackpad-down click : "grip" 
# Vive controller image: https://forums.unrealengine.com/filedata/fetch?id=1111783&d=1460020388
# Vive controller button mappings to keyboard, Oculus Go controller:
#     "application_menu": [X],  (mode 2) trackpad-left click
#     "system"..........: [G],  (mode 2) trackpad-right click
#     "grip"............: [F1], (mode 2) trackpad-down click OR back button (in any mode)
#     "trigger".........: [T],  trigger
#     "trackpad_click"..: [F2], trackpad click 
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

speed_multiplier      = 10
mode_toggle_key       = Key.Space # Key.Tab
speed_toggle_key      = Key.LeftAlt
controller_toggle_key = Key.LeftControl
key_map = [["system", Key.G], ["application_menu", Key.X], ["trigger", Key.T], ["a", Key.V], ["b", Key.B], ["x", Key.N], ["y", Key.M]
, ["grip", Key.F1], ["trackpad_click", Key.F2], ["back", Key.F3], ["guide", Key.F4], ["start", Key.F5]
, ["dpad_left", Key.F6], ["dpad_up", Key.F7], ["dpad_right", Key.F8], ["dpad_down", Key.F9], ["trackpad_touch", Key.F10]]

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
  offset = [0.0, 0.0, 0.0]
  message_time = 0.0
  alvr.two_controllers = True
  controller = 0
  controller_pos = [0.0, 0.0, 0.0]
  for i in range(3):
    alvr.controller_position[controller][i] = alvr.input_controller_position[i]

# change target controller
if controller_toggle_key and keyboard.getPressed(controller_toggle_key):
  controller = 1 - controller
  alvr.message = "%s controller" % ("Left" if controller == 1 else "Right") 
  message_time = time.time()

for k in key_map:
  alvr.buttons[controller][alvr.Id(k[0])] = keyboard.getKeyDown(k[1])

if keyboard.getPressed(mode_toggle_key):
  mode = (mode + 1) % 2
  # show messageo on display
  alvr.message = modeName[mode]
  message_time = time.time()

if time.time() - message_time > 2:
  # remove message after 2 seconds
  alvr.message = ""

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
  # press upper half of trackpad to forward. bottom half to back
  if alvr.input_buttons[alvr.InputId("trackpad_click")]:
    #if alvr.input_buttons[alvr.InputId("trigger")] and alvr.input_trackpad[0] - alvr.input_trackpad[1] > 0.0:
    #  offset = [0.0, 0.0, 0.0]
    #else:
      outvec = rotatevec(alvr.input_controller_orientation, [0, 0, -1, 0])
      speed = 0.002 * sign(alvr.input_trackpad[1])
      if keyboard.getKeyDown(speed_toggle_key):
        speed = speed * speed_multiplier
      for i in range(3):
      	offset[i] += speed * outvec[i]

  alvr.buttons[controller][alvr.Id("trigger")] = trigger_on
elif mode == 0:
  # passthrough mode
  offset = [0.0, 0.0, 0.0]
  alvr.buttons[controller][alvr.Id("trackpad_click")] = alvr.buttons[controller][alvr.Id("trackpad_click")] or alvr.input_buttons[alvr.InputId("trackpad_click")]
  alvr.buttons[controller][alvr.Id("trackpad_touch")] = alvr.buttons[controller][alvr.Id("trackpad_touch")] or alvr.input_buttons[alvr.InputId("trackpad_touch")]
  alvr.buttons[controller][alvr.Id("trigger")] = trigger_on
  alvr.trackpad[controller][0] = alvr.input_trackpad[0]
  alvr.trackpad[controller][1] = alvr.input_trackpad[1]

# You need to set trigger value correctly to get trigger click work
alvr.trigger[controller] = 1.0 if alvr.buttons[controller][alvr.Id("trigger")] else 0.0

alvr.override_head_position          = True
alvr.override_controller_position    = True
alvr.override_controller_orientation = True
for i in range(3):
  if keyboard.getKeyDown(mode_toggle_key):
    alvr.head_position[i] = alvr.input_head_position[i] + offset[i]
  #alvr.controller_position[controller][i] = alvr.input_controller_position[i] + offset[i]
  alvr.controller_orientation[controller][i] = alvr.input_controller_orientation[i]

# For flick of the wrist to work, we must override the default settings for controller movement.
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
    alvr.controller_position[controller][i] = controller_pos[i] + offset[i]
    controller_pos[i] = alvr.input_controller_position[i]

# Button remapping:
# Map "back" button on input to "application_menu" 
alvr.buttons[controller][alvr.Id("application_menu")] = alvr.input_buttons[alvr.InputId("back")]

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
