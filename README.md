# gamepad-midi
A Python app to use gamepad as MIDI device


## MacOS
1. Create "Gamepad" port in the device "IAC Driver" 

        "Audio MIDI Setup" > "Window" > "Show MIDI Studio" > "IAC Driver" > "Ports"
    Check "Device is online"
2. Connect a gamepad (Not every of gamepads are work fine with MacOS, for some of them there are tricks to establish the connection)
3. Run app.py (Make sure that MIDI output works by pressing some buttons. An output in console window should appear)
4. Launch your DAW and search for "IAC Driver (Gamepad)"
5. Have fun!