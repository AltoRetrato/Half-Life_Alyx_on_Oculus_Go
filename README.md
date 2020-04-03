# Playing Half-Life: Alyx on the Oculus Go

## ATTENTION! This is a work in progress!

## Why play Half-Life: Alyx on the Oculus Go?

You can play [Half-Life: Alyx](https://www.half-life.com/en/alyx) with any [Steam-VR compatible system](https://www.half-life.com/en/alyx/vr). While the Oculus Go is not officially supported (has only 3DoF and doesn't have enough buttons), it can be used to play many SteamVR games with the right combinations of hardware, software and configuration.

So far I've managed to play almost the first two chapters of the game on my Oculus Go connected to my PC via Wi-Fi. Of course, the experience is not as fun or intuitive as with a 6DoF headset, but the game is playable and I'm enjoying it. I'd rather buy an Oculus Quest to play the game with, but since I can't buy it now for a reasonable price where I live, the Oculus Go will do.

## Issues

The worst issue so far was that, using the latest stable release of ALVR, the game can't detect the "flick of the wrist" (or "flick of hand") gesture, required to use the gravity gloves. I've provided a new [driver_alvr_server.dll](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/blob/master/driver_alvr_server.dll) that solves this (thanks to information provided by @dnnkeeper).

As soon as I figure out how to complete the game with the Oculus Go I'll rewrite these instructions.

## How?

You will need:
* [Half-Life: Alyx](https://store.steampowered.com/app/546560/HalfLife_Alyx/) and a compatible PC running Windows and [SteamVR](https://store.steampowered.com/app/250820/SteamVR/)
* [ALVR](https://github.com/polygraphene/ALVR/), a free, open source software that allows Gear VR, Oculus Go and Oculus Quest to play SteamVR games
* A nVIDIA GPU which supports NVENC or an AMD GPU which supports AMF VCE (see [ALVR supported GPUs](https://github.com/polygraphene/ALVR/wiki/Supported-GPU))
* [FreePIE](https://andersmalmgren.github.io/FreePIE/) (Programmable Input Emulator)
* Oculus Go (might also work with a Gear VR, but I haven't tested it)
* A 5 GHz Wi-Fi router or USB Wi-Fi dongle adapter, or a USB to Ethernet compatible adapter (not tested)
* The FreePIE script provided here: [Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/blob/master/Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py)
* Optionally, download and edit the ALVR_init.cmd batch file as well to make launching and closing  ALVR easier and faster

Install the [ALVR Client on your Oculus Go](https://alvr-dist.appspot.com/), then on your PC install [SteamVR](https://store.steampowered.com/app/250820/SteamVR/), [ALVR](https://github.com/polygraphene/ALVR/releases) (I recommend [v.2.3.1](https://github.com/polygraphene/ALVR/releases/tag/v2.3.1)) and [FreePIE](https://andersmalmgren.github.io/FreePIE/), following their own instructions. Be sure to follow the [ALVR FreePIE Integration](https://github.com/polygraphene/ALVR/wiki/FreePIE-Integration) instructions.

Replace `ALVR\driver\bin\win64\driver_alvr_server.dll` with the [driver_alvr_server.dll](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/blob/master/driver_alvr_server.dll) provided here - without it, you won't be able to pull or throw objects. Be sure that SteamVR isn't running when you replace the file. Rename the original file to avoid overwriting it, just in case.

At this point I recommend that you just try to start SteamVR and use ALVR. Please see the [ALVR documentation](https://github.com/polygraphene/ALVR/wiki) for details and [troubleshooting tips](https://github.com/polygraphene/ALVR/wiki/Troubleshooting). The only issue I had was some dropped frames that I fixed by either changing the Wi-Fi router settings or simply using another Wi-Fi router.

Another issue you might encounter is bad audio. In my case I had 5.1 selected by default, which apparently isn't supported by ALVR. Select a stereo audio output to solve this (in Windows 10, click the speaker icon in the systray and click on the audio device name to select another, if available). If that doesn't help, you can disable audio in ALVR and use your PC speakers.

To play the game, you can manually follow these instructions (which I recommend for the 1st time) or use a batch file (see below):
* Select a stereo audio output device
* Start FreePIE
* Load and run Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py in FreePIE
* Start ALVR on your PC
* From ALVR, click "Start server"
* Start ALVR on your Oculus Go and connect it to the PC
  * After you connect both, check on ALVR to automatically connect next time
* Start the game in SteamVR

To automate most of the above, download and edit [ALVR_init.cmd](https://github.com/AltoRetrato/Half-Life_Alyx_on_Oculus_Go/blob/master/ALVR_init.cmd) (setting the correct path for your files and optionally audio devices), then:
* Run ALVR_init.cmd
* Start ALVR on your Oculus Go
* When you're done, close the ALVR window on your PC to shutdown ALVR, FreePIE and SteamVR, and revert your sound device to your preferred one

Start the game and, on the 1st run, select "Options > Accessibility > Single Controller: ON", then select the single controller bindings. I also recommend that you create a binding to eject your gun magazine by holding the back button on the Oculus Go controller. Go to `Current binding > Edit > Weapon > (add new binding) Use as button > Hold = Eject Magazine`. You can alternatively use [F1] to simulate the "grip" button in the Vive controller to eject the magazine.

I wrote Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py to allow the required controller bindings and to simulate 6DoF of the controller. Here's how it works:
* There are two modes, "0: default" and "1: fly". You can toggle between then by pressing [SPACE]
* In "0: default" mode:
  * Use the trigger and trackpad on the Oculus Go controller just like on the Vive
    * Trigger to pick up objects, interact, etc.
    * Trackpad left and right to turn around
    * Trackpad bottom to teleport
    * Trackpad center for menu
  * Use the back button on Go as the "Menu" button on the Vive
* In "1: fly" mode:
  * Use the trigger as usual
  * Click the top part of the trackpad to move your hand in the direction pointed by your controller
  * Click the bottom part of the trackpad to move your hand in the opposite direction pointed by your controller
  * Press [SPACE] to go back to "0: default" mode and reset your hand position
  * If you are in "0: default" mode and HOLD [SPACE], you move not only your hand but your head position as well


I guess that is all for now. Feel free to leave comments or suggestions in the Issues section.
