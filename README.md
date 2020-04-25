# Playing Half-Life: Alyx on the Oculus Go

## TL;DR

* Be sure your PC can handle Half-Life: Alyx, you have an [ALVR supported GPU](https://github.com/polygraphene/ALVR/wiki/Supported-GPU) and good 5 GHz Wi-Fi
* Install [ALVR Client on your Oculus Go](https://alvr-dist.appspot.com/) and [ALVR server (portable) on your PC](https://github.com/polygraphene/ALVR/releases/tag/v2.3.1)
* Replace original (and buggy) `ALVR\driver\bin\win64\driver_alvr_server.dll` with this [driver_alvr_server.dll](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/raw/master/driver_alvr_server.dll) (after downloading it, right-click the DLL, select Properties, check Unblock)
* Install [FreePIE](https://andersmalmgren.github.io/FreePIE/)
* Use [Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py](https://raw.githubusercontent.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/master/Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py)
* Optionally, edit and use [ALVR_init.cmd batch file](https://raw.githubusercontent.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/master/ALVR_init.cmd) to launch at once everything you need to play.
* Enjoy!

## Why play Half-Life: Alyx on the Oculus Go?

You can play [Half-Life: Alyx](https://www.half-life.com/en/alyx) with any [Steam-VR compatible system](https://www.half-life.com/en/alyx/vr). While the Oculus Go is not officially supported, it can be used to play many SteamVR games with the right hardware, software and configuration.

I've completed the game, playing on my Oculus Go connected to my PC via Wi-Fi. Of course, the experience is certainly not as fun or intuitive as with a 6DoF headset (Oculus Go has only 3DoF and doesn't have enough buttons), but the game is fully playable and I enjoyed it immensely. I'd rather buy an Oculus Quest to play the game with, but since I can't buy it now for a reasonable price where I live, the Oculus Go will do.

## How?

You will need:
* [Half-Life: Alyx](https://store.steampowered.com/app/546560/HalfLife_Alyx/) and a compatible PC running Windows and [SteamVR](https://store.steampowered.com/app/250820/SteamVR/)
* [ALVR](https://github.com/polygraphene/ALVR/), a free, open source software that allows Gear VR, Oculus Go and Oculus Quest to play SteamVR games
* The latest stable release of ALVR can't detect the "flick of the wrist" (or "flick of hand") gesture, required to use the gravity gloves. I've provided a new [driver_alvr_server.dll](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/raw/master/driver_alvr_server.dll) that solves this (thanks to information provided by @dnnkeeper).
* A nVIDIA GPU which supports NVENC or an AMD GPU which supports AMF VCE (see [ALVR supported GPUs](https://github.com/polygraphene/ALVR/wiki/Supported-GPU))
* [FreePIE](https://andersmalmgren.github.io/FreePIE/) (Programmable Input Emulator)
* Oculus Go (might also work with a Gear VR, but I haven't tested it)
* A 5 GHz Wi-Fi router or USB Wi-Fi dongle adapter, or a USB to Ethernet compatible adapter (not tested)
* The FreePIE script provided here: [Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py](https://raw.githubusercontent.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/master/Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py)
* Optionally, download and edit the [ALVR_init.cmd batch file](https://raw.githubusercontent.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/master/ALVR_init.cmd) as well to make launching and closing  ALVR easier and faster

Install the [ALVR Client on your Oculus Go](https://alvr-dist.appspot.com/), then on your PC install [SteamVR](https://store.steampowered.com/app/250820/SteamVR/), [ALVR v.2.3.1](https://github.com/polygraphene/ALVR/releases/tag/v2.3.1) and [FreePIE](https://andersmalmgren.github.io/FreePIE/), following their own instructions. Be sure to follow the [ALVR FreePIE Integration](https://github.com/polygraphene/ALVR/wiki/FreePIE-Integration) instructions.

Replace `ALVR\driver\bin\win64\driver_alvr_server.dll` with the [driver_alvr_server.dll](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/raw/master/driver_alvr_server.dll) provided here - without it, you won't be able to pull or throw objects. After downloading it, right-click the file, select Properties and check Unblock. Be sure that SteamVR isn't running when you replace the file. Rename the original file to avoid overwriting it, just in case. If you'd rather build ALVR yourself, see [RemoteController.patch](RemoteController.patch).

At this point I recommend that you just try to start SteamVR and use ALVR. Please see the [ALVR documentation](https://github.com/polygraphene/ALVR/wiki) for details and [troubleshooting tips](https://github.com/polygraphene/ALVR/wiki/Troubleshooting). The only issue I had was some dropped frames that I fixed by either changing the Wi-Fi router settings or simply using another Wi-Fi router.

Another issue you might encounter is bad audio. In my case I had a 5.1 output selected by default, which apparently isn't supported by ALVR. Select a stereo audio output to solve this (in Windows 10, click the speaker icon in the systray and click on the audio device name to select another, if available). If that doesn't help, you can disable audio in ALVR and use your PC speakers. You can automatically change the audio output using the batch file I provided, but you will also need to download [NirCmd](https://www.nirsoft.net/utils/nircmd.html).

To play the game, you can manually follow these instructions (which I recommend for the 1st time) or use a batch file (see below):
* Select a stereo audio output device
* Start FreePIE
* Load and run Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py in FreePIE
* Start ALVR on your PC
* From ALVR, click "Start server"
* Connect the Oculus Go to the same Wi-Fi /router used by your PC
* Start ALVR on your Oculus Go, then connect it using the ALVR interface on your PC
  * After they are connect, check on ALVR to automatically connect next time
* Start the game in SteamVR

To automate most of the above, download and edit [ALVR_init.cmd](https://raw.githubusercontent.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/master/ALVR_init.cmd) (setting the correct path for your files and optionally audio devices), then:
* Run ALVR_init.cmd
* Start ALVR on your Oculus Go
* When you're done, close the ALVR window on your PC to shutdown ALVR, FreePIE and SteamVR, and revert your sound device to your preferred one

Start the game and, on the 1st run, select "Options > Accessibility > Single Controller: ON", then select the single controller bindings. I also recommend that you create a binding to eject your gun magazine by holding the back button on the Oculus Go controller. Go to `Current binding > Edit > Weapon > (add new binding) Use as button > Hold = Eject Magazine`. You can alternatively use [F1] to simulate the "grip" button in the Vive controller to eject the magazine. You also need to enable "Options > Accessibility > Height Adjust: Crouch".

I wrote Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py to allow the required controller bindings and to simulate 6DoF of the controller. Here's how it works:
* There are two modes, "0: default" and "1: fly". You can toggle between then by pressing [SPACE]
* In "0: default" mode:
  * Use the trigger and trackpad on the Oculus Go controller just like on the Vive:
    * Trigger to pick up objects, interact, etc.
    * Trackpad left and right to turn around
    * Trackpad bottom to teleport
    * Trackpad center click for crouching / standing
    * Trackpad center hold for menu
  * Use the back button on Go as the "Menu" button on the Vive (click activate grenades, reload weapons when pointing to your shoulder, etc.)
  * Hold the back button to eject a magazine
* In "1: fly" mode:
  * Use the trigger and back buttons as usual
  * Click the top part of the trackpad to move your hand in the direction pointed by your controller
  * Click the bottom part of the trackpad to move your hand in the opposite direction pointed by your controller
  * Press [SPACE] to go back to "0: default" mode and reset your hand position
  * If you are in "0: default" mode and HOLD [SPACE], you move not only your hand but your head position as well
  * Hold [ALT] for faster flying speed

## Gear VR controller

You can optionally use a Gear VR controller instead of the keyboard (but be aware that it might not always properly register button clicks, specially when you are between the controller and the PC Bluetooth adapter). Your PC Bluetooth adapter must support BLE (Bluetooth Low Energy) devices (i.e., must support at least Bluetooth 4.0, but not all Bluetooth 4.0 dongles support BLE). Click a controller button to wake it up before starting the FreePIE script. Look in the FreePIE console to see if your Gear VR controller is connected. If it disconnects, restart the script. To enable the Gear VR controller in FreePIE, download and install the [FreePIEVRController DLL plugin](https://github.com/polygraphene/FreePIEVRController/releases) in the FreePIE plugins folder, and don't forget to unblock it (right-click the file, select Properties, check Unblock).

These are the functions currently provided by each Gear VR button:
* [Trigger] toggles between modes; hold to move hand & head positions when flying
* [Touchpad click] for faster flying speed
* [Back] to reset head & hand positions
* [Vol.Up] and [Vol.Down] to move hand position, in either mode

## Issues

The only binding I could not make work so far is double-clicking. This is used for "Toggle Burst Fire", but since it is not required to complete the game, I didn't spend time researching the cause.

## Final words

I guess that is all for now. Feel free to leave comments or suggestions in the Issues section.
