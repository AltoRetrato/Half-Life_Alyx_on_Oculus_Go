@echo off

REM This .CMD automate tasks for initing & shutting down SteamVR via ALVR,
REM such as opening/closing FreePIE (and running its related script) and
REM configuring system audio settings.

REM Please edit the paths of the files.

REM If you want to also select the audio device (and restore it at the end),
REM download nircmd from https://www.nirsoft.net/utils/nircmd.html
REM (links at the end of the page). Otherwise, you can comment out the lines
REM invoking nircmd.exe with "REM".

:ON
echo Changing audio output device to "Realtek Digital Output"
C:\Users\Ric\Documents\CMDs\nircmd.exe setdefaultsounddevice "Realtek Digital Output"

echo Starting FreePIE
start /B "FreePIE" "C:\Program Files (x86)\FreePIE\FreePIE.exe" C:\Users\Ric\Desktop\VR\ALVR\freepie-samples\Ric's_Half-Life_Alyx_FreePIE_ALVR_script.py /run

echo Starting SteamVR
start /B "SteamVR" "E:\Steam\Steam.exe" -applaunch 250820

echo Starting ALVR
start /B /WAIT "ALVR" "C:\Users\Ric\Desktop\VR\ALVR\ALVR.exe"

:OFF
echo Shutting down FreePIE
taskkill /IM FreePIE.exe

echo Shutting down SteamVR
taskkill /T /IM vrserver.exe /IM vrmonitor.exe /IM vrwebhelper.exe

echo Changing audio output device back to "Speakers"
C:\Users\Ric\Documents\CMDs\nircmd.exe setdefaultsounddevice "Speakers"

:END
echo.
timeout /T 10