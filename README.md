Joystick Gremlin EX
================



## Contents

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Changelog](#changelog)
- [Virus false-positives](#virus-false-positives)
- [Releases](#releases)
- [General](#general)
- [Compatibility](#compatibility)
- [There be dragons ahead!  ](#there-be-dragons-ahead)
   * [Support](#support)
   * [History](#history)
- [Installation](#installation)
- [Automatic Input detection](#automatic-input-detection)
      + [Button detect only overrides](#button-detect-only-overrides)
- [Remote control feature](#remote-control-feature)
      + [Master machine setup](#master-machine-setup)
         - [Local mode](#local-mode)
         - [Broadcast mode](#broadcast-mode)
         - [Concurrent mode](#concurrent-mode)
      + [Client machine setup](#client-machine-setup)
   * [Master remote control functions](#master-remote-control-functions)
- [Profile mapping](#profile-mapping)
   * [Automatic activation](#automatic-activation)
   * [Keep profile active when focus is lost](#keep-profile-active-when-focus-is-lost)
   * [Mode selection](#mode-selection)
   * [Caveats with automation](#caveats-with-automation)
   * [Caveats with loading to the prior mode](#caveats-with-loading-to-the-prior-mode)
- [Copy/Paste operations](#copypaste-operations)
- [Devices](#devices)
   * [HID devices](#hid-devices)
   * [Keyboard (+Mouse) device](#keyboard-mouse-device)
      + [Virtual Keyboard](#virtual-keyboard)
         - [Selecting a key](#selecting-a-key)
         - [Shift state](#shift-state)
         - [Select single](#select-single)
         - [Selected keys](#selected-keys)
         - [Listen button](#listen-button)
         - [Pass-through](#pass-through)
      + [Special considerations](#special-considerations)
   * [MIDI device](#midi-device)
      + [MIDI inputs](#midi-inputs)
      + [MIDI trigger modes](#midi-trigger-modes)
      + [Changing modes](#changing-modes)
      + [MIDI conflicts](#midi-conflicts)
      + [MIDI ports](#midi-ports)
      + [Network MIDI](#network-midi)
      + [Using MIDI from touch surfaces](#using-midi-from-touch-surfaces)
      + [MIDI controllers](#midi-controllers)
      + [MIDI troubleshooting](#midi-troubleshooting)
   * [OSC device (Open Sound Control)](#osc-device-open-sound-control)
      + [OSC port](#osc-port)
      + [OSC inputs](#osc-inputs)
         - [OSC Trigger modes](#osc-trigger-modes)
      + [Changing modes](#changing-modes-1)
- [VJoyRemap action ](#vjoyremap-action)
   * [VJoyRemap button press actions](#vjoyremap-button-press-actions)
   * [VJoyRemap axis mapping actions](#vjoyremap-axis-mapping-actions)
- [Map to mouse EX action](#map-to-mouse-ex-action)
- [Map to keyboard EX action](#map-to-keyboard-ex-action)
      + [Dragons](#dragons)
- [Range container](#range-container)
      + [Ranges](#ranges)
      + [Include/exclude flag](#includeexclude-flag)
      + [Symmetry](#symmetry)
      + [Latching](#latching)
      + [Dragons](#dragons-1)
- [Button Container](#button-container)
      + [Usage tips](#usage-tips)
      + [Pressed block](#pressed-block)
      + [Release block](#release-block)
- [TempoEx Container (tempo with chain)](#tempoex-container-tempo-with-chain)
- [Plugin Script enhancements](#plugin-script-enhancements)
      + [@gremlin.input_devices.gremlin_start](#gremlininput_devicesgremlin_start)
      + [@gremlin.input_devices.gremlin_stop](#gremlininput_devicesgremlin_stop)
      + [@gremlin.input_devices.gremlin_mode](#gremlininput_devicesgremlin_mode)
      + [@gremlin.input_devices.gremlin_state](#gremlininput_devicesgremlin_state)
- [Recipes](#recipes)
   * [One way or two way switch to two way switch / three way switch](#one-way-or-two-way-switch-to-two-way-switch-three-way-switch)
   * [Long/short press - buttons or keyboard](#longshort-press-buttons-or-keyboard)
      + [To setup concurrent button presses (hold the short press while long press is active)](#to-setup-concurrent-button-presses-hold-the-short-press-while-long-press-is-active)
      + [To setup a latched short, then long button press with only one button active](#to-setup-a-latched-short-then-long-button-press-with-only-one-button-active)
   * [Scripting logic](#scripting-logic)
      + [Attaching a function to a hardware event](#attaching-a-function-to-a-hardware-event)
   * [Recommended Resources](#recommended-resources)
         - [VJOY virtual joystick driver ](#vjoy-virtual-joystick-driver)
         - [OSC support in Joystick Gremlin from TouchOSC](#osc-support-in-joystick-gremlin-from-touchosc)
         - [HIDHIDE](#hidhide)
         - [Hexler TouchOSC](#hexler-touchosc)
- [Troubleshooting guide ](#troubleshooting-guide)
   * [HID devices - detection / random disconnects](#hid-devices-detection-random-disconnects)
   * [HID troubleshooting tips ](#hid-troubleshooting-tips)
   * [HIDHide troubleshooting](#hidhide-troubleshooting)
   * [Checking your mappings](#checking-your-mappings)
   * [GremlinEx has been tested with ](#gremlinex-has-been-tested-with)
   * [Sample scripts](#sample-scripts)
   * [OSC (open stage control) info](#osc-open-stage-control-info)
   * [Python dependencies](#python-dependencies)

<!-- TOC end -->

<!-- TOC --><a name="changelog"></a>
# Changelog


13.40.14ex

This release adds major new features, including some minor changes in UI functionality, and a few more QOL (quality of life) enhancements.

- **New virtual keyboard** dialog to simplify key and mouse button selection. The updated editor supports hidden keys such as F13 to F24 and enables mouse buttons to be used as any "key" input to simplify mapping. (QOL)
- Revamped keyboard input device and UI with virtual keyboard with mouse input support with multiple key latching.  Profiles using the old style should convert automatically to the new style.  Inputs can be added, edited and removed.  Latching (concurrent keys pressed) allows for complex and unusual keyboard input combinations to trigger actions including latching with mouse button and mouse wheel inputs.
- Revamped keyboard conditions on actions or containers:  a keyboard condition now uses the new virtual keyboard editor and allows for multiple latched keys and mouse button triggers. (QOL)
- **New MIDI input device** - GremlinEx can now map MIDI events to GremlinEx actions. The new MIDI inputs can be added, edited and removed in the MIDI device tab. 
- **New OSC (Open Sound Control) input device** - GremlinEx can now map OSC events to GremlinEx actions. The new OSC inputs can be added, edited and removed from the OSC device tab.
- New Gated Axis functionality for some actions (SimConnect axis mapping as well as VJoy axis mapping - new axis mode).  Gates axes have the notion of "gates", or points along an axis that can be used to trigger one or more sub-actions and modify the axis value output behavior.
- Improved icon reload speed (speeds up the UI load/refresh/update)
- New file menu for opening Explorer to the current profile folder (QOL)
- New file menu for opening the profile XML in a text editor (it will save the profile first) (QOL)
- New mouse event drop down selector in map to mouse ex: adds a mouse event selection drop down so mouse actions can be selected by name rather than mouse input only.  
- Action container will now scroll horizontally if the action is too wide to fit based on windows size / UI scaling options. (QOL)
- Profiles can be saved even if one or more actions are not configured (QOL)
- Updated profile to application (process) mapping in the options dialog (QOL)
- Options dialog remembers which tab it was last in (QOL)
- Options dialog has a close button (QOL)
- Options dialog saves profile mapping information on close (QOL)
- Pressing F5 in the UI will activate the current profile (QOL)
- New configuration dialog for the loaded profile, separate from the global options (QOL).  This lets you quickly set profile activation options.
- New option to force numlock off when a profile starts to help with the more complex latching that use numpad keys.
- Added joystick input value display on axis inputs - shows an axis bar with the current axis value in the input (QOL) - can be toggled in options.
- Update to Python 3.12.5

6/6/24 - 13.40.13ex (h) **potentially breaking change**

- GremlinEx will now more gracefully handle DLL errors and check driver and DLL versions.  If the driver and DLL versions are not at minimum levels expected, an error box will be displayed and will exit the app to avoid further errors due to mismatched versions.

GremlinEx requires vJoy device driver 12.53.21.621 (VJOY release 2.1.9.1 minimum).    The distribution includes the interface DLL for 2.1.9.1, but not the software which by licensing agreement cannot be included in the GremlinEx distribution.  The latest version can be found here:

The vJoy version can be found here: https://sourceforge.net/projects/vjoystick/files/Beta%202.x/2.1.9.1-160719/

The version of HIDHide can be found here: https://github.com/nefarius/HidHide/releases

There are probably more hardening that can be done to validate the environment.


When installing a new version of vJoy or HIDHide, uninstall the old versions first, and reboot between sessions to make sure files are removed and there will not be a conflict on installation.  There are documented issues when failing to reboot after uninstalling either HIDHide or vJoy.
 
Sequence wise, install vJoy first, then HIDHide.

Updated Device Information dialog to use a table format that is user resizeable.  Right click on any cell to copy its contents to the clipboard.

Bug fix for device removal / addition while a profile is running.

If a device is referenced by a script or profile and cannot be found as GremlinEx is running, or if it was added/removed dynamically while GremlinEx is running, this will no longer throw an exception.  The issue will be logged as a warning to the log file and calls using that device will just be ignored.  Plugin scripts should ensure they now check the return value of any proxy call when looking for a device as the call my return null (None) if the device cannot be found.  It is generally discouraged to change hardware configurations while GremlinEx is running, or change device hardware IDs as those are stored in profiles, and will be ignored if the ID is no longer found.  
Missing IDs in profile will be logged to the log file and a message box displayed at load time.


6/2/24 - 13.40.13ex (a) **potentially breaking change**

- Changed default profile folder to *Joystick Gremlin Ex* to use a different folder from the original *Joystick Gremlin* folder to avoid conflicts.  If the new profile folder does not exist, GremlinEx will, for convenience, make copy the original profile folder  to the *Joystick Gremlin Ex* folder.  The path used is %userprofile%\Joystick Gremlin Ex

6/2/24 - 13.40.13ex

- added copy/paste for actions and containers (experimental) - actions can be copied (new button on title bar) and can be pasted via a new button wherever actions can be added).  Containers can also be copied and pasted where containers can be added.  New option to persist clipboard data between sessions.

Because the name "dill" conflicts with the Python module "dill", renamed to "dinput".

5/31/24 - added TempoEx container and resolved a macro call bug

5/27/24 - added Button container and improved handling of automatic switching

4/8/24 - added troubleshooting guide and sample scripts for advanced GremlinEx scripting via plugins

4/12/24 - bug fixes (see release notes on issues resolved)

4/18/24 - adding range container and keyboard mapper EX (wip - may break!)
Introduction

------------


<!-- TOC --><a name="virus-false-positives"></a>
# Virus false-positives

GremlinEx uses a common tool called PyInstaller as its packaging option.  Pyinstaller is unfortunately known to create false-positives with some malware detection tools, because of how it works and this is unfortunately not an issue I can solve easily while it concerns me greatly.  The good news is, it happens rarely.

There is no known solution as the false positive, if it occurs, is unfortunate yet common to python solutions using PyInstaller (Google it) and must be fixed by the scanning software provider. I can make a few suggestions however: 

If you don't trust the software, you can run it through www.virustotal.com and it will tell you how many malware solutions detect the false positive.  You will see that very few, if any, detect this issue.

You can run the code from source, in which case you will need to make sure you have the Python environment installed and its dependencies.  You can run the joystick_gremlin.py file by itself using python joystick_gremlin.py at the command line.  The dependencies are listed in requirements.txt.

You can build the executable yourself using the deploy.bat file in the source folder which is the mechanism I use to build the EXE from source. Unfortunately this doesn't seem to fix the issue for many people even if you are the one building on your own computer.

If the false-positive is reported by your scanning solution, you can make an exception in your A/V solution and mark the .exe as an exception to the scanning, until your A/V solution corrects the false-positive detection.  This appears to be the usual recourse for python projects packaged to .exe using PyInstaller from my research to date.

Some have suggested the code should be signed, however I point out this utility is free, its packaging is provided as a convenience, the work is the product of hundreds of development hours, and I am not currently in a position to incur a recurring expense for a free tool to sign the code in the hope it bypasses the rare false-positive detection, given the options that are provided and the rarity of the detection, which itself is due to misreporting by the scanning software.

I will continue to monitor this issue but please use one of the above workarounds if this happens.

<!-- TOC --><a name="releases"></a>
# Releases

Releases, including pre-releases can be found [here on GitHub](https://github.com/muchimi/JoystickGremlinEx/releases).  Be aware the release version may not be the most up to date as GitHub hides pre-releases by default.

Pre-releases are mostly (proposed) bug fixes but also can contain work-in-progress items and

<!-- TOC --><a name="general"></a>
# General

GremlinEx started as a fork of the excellent original Gremlin project by WhiteMagic.  For general original Joystick Gremlin documentation - consult https://whitemagic.github.io/JoystickGremlin/

Gremlin EX adds a number of features to the original, including some bug fixes or quality of life enhancements I wanted to see, or were suggested to me.  Many parts of the original were rewritten although the core design and mechanics have remained the same, a good thing.  The major changes are below.

- Update to x64 bit from x32 bit
- Update to Python 12.x (improved execution speed over Python 10)
- Update to QT6 UI framework
- Improved stability when loading a plugin that has an error on load
- Remote data control of another GremlinEx client on the local network (this lets you send input from one box from hardware connected to a different box on the network) with low latency (typically 20ms or so)
- OSC message handling (for touch screen support going to Gremlin via TouchOSC for example) - this lets you implement "game glass" functionality easily while working around Windows' limitation with touch screen control surfaces on the same box
- VjoyRemap plugin for enhanced button/axis Vjoy mapping  
- MapToMouseEx action plugin for enhanced mouse control  
- Range container for mapping axis ranges to actions easily
- MapToKeyboardEx action plugin for enhanced keyboard control with separate make/break and delay functionality
- Button container - provides a direct way perform actions on a raw button press or release, which is helpful for on/off and three-way buttons
- MIDI input mapping - GremlinEx can listen to MIDI messages and trigger actions based on those.
- Copy/Paste containers and actions between inputs.
- Save profiles in progress for which actions are not necessarily all configured.
- Use of more icons and tooltips to make GremlinEx more intuitive to navigate.


I suggest you make VjoyRemap the default action in the options panel as this plugin is what provides many enhancements over the default Remap plugin.  Same for mouse output - MapToMouseEx provides enhanced options for the mouse macro functions.

This said, the default plugins are all functional but they won't be aware of the new features in GremlinEx.

<!-- TOC --><a name="compatibility"></a>
# Compatibility

GremlinEx will load original Gremlin profiles and copy them to a new profile folder called *Joystick Gremlin Ex*.  Profiles saved with GremlinEx may however not be compatible with the original.

While the core functionality looks similar, GremlinEx adds new container types, new input types and in some cases processes things differently.

Original plugins have not been touched unless core GremlinEx code and behavior changes broke them.  Updated versions will typically be marked Ex - these actions will have similar functionality but may add a few more features.

User scripts for GremlinEx also gain a few new functions and decorators to help with script management and state awareness in particular.



<!-- TOC --><a name="there-be-dragons-ahead"></a>
# There be dragons ahead!  

I updated this code repository for my own purpose as I ran across my hardware cockpit needs for my PC based simulators and thought to myself - hey - would love if this did [that]!  I was quickly confined though to the base functionality and realized soon that some deeper surgery was needed.  I also wanted the code to use current platform tools as there is for example a significant boost in performance just by using a new Python environment.

As such, the code may have some bugs and other things I'm missed in my own testing, so please report issues you encounter as you find them and I'll do my best to fix them.

<!-- TOC --><a name="support"></a>
## Support

As this is on my free time, support is on a best effort basis.  To help that, please create and/or update an existing GitHub issue and do include screenshots, describe what you're trying to do, any steps to reproduce, and attach an example  profile as that will help a lot.   

 
I am using this tool daily for all my flight sims so I know the parts I'm using are working - but Gremlin's premise is to be very flexible and that will definitely lead to situations I haven't tried yet, or that the code just blows up on because it never came up.  My goal however is to get it fixed.



<!-- TOC --><a name="history"></a>
## History


The core Gremlin repository was substantially modified in some areas to support remote control, including some new events, adding improved support for user plugin  scripts (so they are aware of state information for example). Some UI elements were also modified a bit to improve the visuals and to simplify certain aspects of Gremlin. For example, all buttons support a release action without going through more complex conditions, as in my book a check box is simpler to setup in this use-case than to go through an additional three screens. This made it much simpler for me to map physical switches on throttles that have a single state to multi-state and do what used to be complex mappings essentially a checkbox affair.

I have attempted to use the base project as much as possible, and I am grateful to WhiteMagic and his excellent ideas and structure as Gremlin is simply the best mapping utility I have ever seen or used in decades of simulation and hardware input mapping to games.  The architecture is also excellent and made my modifications very simple.

I am using this code daily for my simulation needs but that's not a guarantee everything works as expected.  Feedback welcome!  

<!-- TOC --><a name="installation"></a>
# Installation

The release includes a zip file that contains a packaged version of the Joystick Gremlin Ex python scripts as a convenient .EXE.   Place the contents of the zip file in a folder, recommend C:\Joystick Gremlin Ex or other suitable location.  

On first run, starting with 13.40.13x, GremlinEx will create a profile folder called Joystick Gremlin Ex in the %userprofile% folder.   If this folder does not exist, it will be created, and if the original profile folder for Joystick Gremlin is found, a copy of that profile folder will be made to keep the files separate.  GremlinEx may include additional configuration, plugins, actions and scripting commands the original Joystick Gremlin will not understand.


The profile path is *%userprofile%\Joystick Gremlin Ex*



<!-- TOC --><a name="automatic-input-detection"></a>
# Automatic Input detection

GremlinEx can auto-highlight hardware joystick input devices by clicking a button or moving an axis on them.   This eliminates the guesswork on how the hardware maps to buttons or axes.

Automatic detection is only active when a profile is not running.

When in this mode, GremlinEx will attempt to display the correct input - I say attempt because it can get confused sometimes with multiple active concurrent inputs.

The default behavior is it waits for an axis or a button to be activated before displaying anything, so the initial load up UI may not reflect the input until it's touched again.

GremlinEx has a built in protection against multiple inputs, but will display the last detected input if multiple inputs were sent.

There are three options that control this behavior in the GremlinEx options panel:

| Option      | Description |
| ----------- | ----------- |
| Highlight currently used input (axis + button) | Will switch focus to the input device for axis or button changes - this can make it difficult to just pick a button|
| Highlight currently used buttons | Detects button changes only (axis movement is ignored but can be overriden - see below (this is recommended) | 
| Highlight swaps device tabs | Changes input tabs automatically (this is a recommended) |




<!-- TOC --><a name="button-detect-only-overrides"></a>
### Button detect only overrides

A pair of modifiers can be used to modify how input is detected.  

| Option      | Description |
| ----------- | ----------- |
| Left shift | If you hold the left shift key, GremlinEx will track axes instead of just buttons regardless of the options selected .|
| Left control | If you hold the left control key, GremlinEx will only track axes  regardless of the options selected .|

Recommend that you set the default behavior is to track buttons only as it's very easy to trigger an axis by pressing a button because many hardware devices are very sensitive. Use the  left shift or control key to modify that behavior on the fly.

Note that whatever is first detected will go to that item (axis or button) if nothing is selected.  This is on purpose to pick a starting point.

Holding the left-shift key down when in button detect mode temporarily enables axis detection as well as button detection.  This is the same as the first option in the table above.

Holding the left-shift key and the left-control key when in button detect mode temporarily enables exclusive axis detection and ignores button presses.  This is helpful when you have a hardware axis that also has detents along the way that send button inputs.  In this mode, these buttons will be ignored. 


<!-- TOC --><a name="remote-control-feature"></a>
# Remote control feature

GremlinEx adds a feature to link multiple GremlinEx instances running on separate computers.  This is helpful to share a single set of controls and a single profile on a master machine to one or more client machines on the local network.

The use-case for this need came up in a couple of scenarios in my own setup:  I wanted to be able to share my hardware panels and input controllers with another machine without having to duplicate them.

Events sent over the network include all GremlinEX output functions:
- VJOY joystick axis events (when an axis is moved)
- VJOY joystick button events
- keyboard output events (press/release keys including extended keys)
- mouse output events (pres/release mice button 1 to 5, mouse wheel events, and mouse motion events)
- Gremlin macro outputs

By output events, we mean that inputs into GremlinEx are not broadcast to clients, only events that GremlinEx outputs are synchronized with clients.  

To use the remote control features, it is intended you use the new plugins VjoyRemap and MapToMouseEx


<!-- TOC --><a name="master-machine-setup"></a>
### Master machine setup

The master machine is the machine responsible for broadcasting control events to clients on the local network.  Thus it will typically be the primary system with all the physical hardware managed by GremlinEx.

The broadcast machine or master system will have the broadcast option enabled and an available UDP port setup (default 6012).  When the broadcast feature is enabled, GremlinEx will broadcast all output events.

Important: to broadcast, the option must be enabled in the checkbox, and the GremlinEx profile must also have enabled the broadcast functionality on.  This is needed because when GremlinEx first starts, it defauts to local control only.

Profile commands can be mapped via the VjoyRemap plugin to control whether GemlinEx sends outputs to the local (internal) or clients, or both concurrently.

While more than one master machine can broadcast, it's recommended to only have one.  Multiple machines will allow more than one machine to send broadcast commands to clients for unique setup needs.

The enable speech checkbox can be selected for GremlinEx to send a verbal mode change event whenever local/remote mode control is changed in case the GremlinEx window is not visible.

GremlinEx shows what output mode is active in the status bar.


<sup>GremlinEx options setup for a broadcast machine:</sup>

![](img/server_options.jpg)


<!-- TOC --><a name="local-mode"></a>
#### Local mode

In this mode, GremlinEx sends VJOY, keyboard and mouse events to the local machine.

The status bar displays

![](img/local_control.jpg)


<!-- TOC --><a name="broadcast-mode"></a>
#### Broadcast mode

In this mode, GremlinEx sends VJOY, keyboard and mouse events to clients on the network.    The clients must have the remote control checkbox enabled, match the port number, and have a profile running (empty profile is fine) to respond to the broadcast events.


The status bar displays

![](img/remote_control.jpg)

<!-- TOC --><a name="concurrent-mode"></a>
#### Concurrent mode

GremlinEx can send to the local and remote clients at the same time (concurrent mode) by sending the Concurrent command. 



<!-- TOC --><a name="client-machine-setup"></a>
### Client machine setup

Each GremlinEx client needs to have the remote control option enabled in options to be able to receive events from the master machine.   The master machine must also be setup to broadcast these events.

The client must be in run mode to accept broadcast events, and the profile can be empty.  No profile needs to be loaded on the client when the client is in remote control mode.

Clients will only output to VJOY outputs that match the master.  So if the client has the same setup for VJOY (number of VJOY devices, button counts and hat counts) as the master machine, all VJOY events will be synchronized with the master machine.   This is the recommended setup.   

Clients will ignore events for devices that do not exist on the client (such as an invalid VJOY device number, or an invalid button for that defined device).

<sup>GremlinEx options setup for a client:</sup>

![](img/client_options.jpg)

The enable remote control checkbox is checked, and the port (default 6012) must match the broadcast machine's port.

<!-- TOC --><a name="master-remote-control-functions"></a>
## Master remote control functions

Local and broadcast (sending output to remote GremlinEx instances on network machines) control can be enabled or disabled via GremlinEx commands bound to a joystick button (or in script).

Commands are available in the VjoyRemap plugin when bound to a joystick button and available from the drop down of actions for that button.

<!-- TOC --><a name="profile-mapping"></a>
# Profile mapping

GremlinEx has multiple options to automate the loading and activation of profiles based on what process has the current focus (meaning, the active window).


![](gremlin_ex_profile_options.png)

<!-- TOC --><a name="automatic-activation"></a>
## Automatic activation

If a process (.exe) is mapped to a specific profile (.xml), GremlinEx can automatically load this profile when the process has the focus at runtime.  This only works when a GremlinEx is in "run" mode - so a profile was loaded and activated.

If configured, GremlinEx will load the mapped profile corresponding to the process (.exe) automatically in the background.  Depending on the complexity of the profile, GremlinEx may take a few seconds to become active as it loads the process and activates it.

The automatic load occurs whenever GremlinEx detects a process focus change.

<!-- TOC --><a name="keep-profile-active-when-focus-is-lost"></a>
## Keep profile active when focus is lost

This mode is used to ensure GremlinEx keeps the profile running even if the process it is mapped to no longer has the primary focus.   This happens, for example when you alt-tab, or when you activate another window.  The recommendation is to leave this option enabled.

<!-- TOC --><a name="mode-selection"></a>
## Mode selection

When automatic profile load is enabled, GremlinEx has the option to override the default "startup" mode of a profile.  This is by default, the top level mode.  There are two options of interest:

- Activate a default mode when the profile is activated (this is the normal mode)
- Activate the last mode used when the profile was last activated (this is the alternate mode).  If this is enabled, the default mode setting is ignored.  The first mode used will be the default mode if the mode has not been changed before.

In addition to this, the profile itself provides actions that can switch modes.


<!-- TOC --><a name="caveats-with-automation"></a>
## Caveats with automation

GremlinEx is not aware of anything except what process has the current focus, and what you've configured in the profile options.  It's completely possible that you will experience conflicts if you have programmed these in, or constant loading/reloading.

To guard against this behavior, here are things that are not recommended:

- have two processes (such as games) each associated with an automatic load profile and constantly changing focus between the two. This will cause a profile reload/reset and new mode activation whenever the focus changes.

- attach a profile to a non-game, such as a background process.

The recommended approach is to only run one mapped process at a time, ensure the profile remains active if you alt-tab or switch to another window on multi-monitor setups.

<!-- TOC --><a name="caveats-with-loading-to-the-prior-mode"></a>
## Caveats with loading to the prior mode

Loading the prior mode may not necessarily be expected, as it will vary with the last known used mode.   This can be confusing and unexpected, but it can be helped by ensuring that you tell GremlinEx to say what mode it's in whenever a profile starts.



<!-- TOC --><a name="copypaste-operations"></a>
# Copy/Paste operations

Starting with GremlinEx 13.40.13ex, copy/paste operations are supported on actions and containers.

To copy an action or container, click the copy button in the title bar.

To paste and action or container, click on the paste button next to the add action or add container.

Pasting is not possible if the container or action is not permitted for the type of input being mapped.

You can persist a copy operation between GremlinEx sessions by checking the option in the options dialog.  This will save the data to the profile folder, and it will be available at the next session.

If the persist option is not checked, GremlinEx will use whatever data is in the Windows clipboard from the last copy operation in GremlinEx.

![](copy_paste_operations.png)


<!-- TOC --><a name="devices"></a>
# Devices

<!-- TOC --><a name="hid-devices"></a>
## HID devices

GremlinEx will show all detected game controllers in tabs located at the top of the UI.  These are the raw input devices, either buttons, hats or axes.

<!-- TOC --><a name="keyboard-mouse-device"></a>
## Keyboard (+Mouse) device

GremlinEx has an updated special Keyboard device that allows you to map keyboard and mouse button as inputs to trigger actions and containers. 

![](gremlin_ex_keyboard.png)

GremlinEx allows you to map unusual function keys F13 to F24 and any QWERTY keyboard layouts (no support for other layouts as of yet), as well as mouse input buttons including mouse wheel actions. 

#### Keyboard inputs

![](keyboard_input.png)

Keyboard inputs, as with joystick inputs are shown on the left panel in GremlinEx in the keyboard tab.  Inputs can be added, removed and edited (configured).  If an input is removed, it will remove any associated mappings.  A confirmation box will pop up if an input with content will be deleted.

Use the action and container copy/paste feature to duplicate actions between inputs.

#### Scan Codes

Gremlin Ex has an option to display keyboard scan codes that will be heard by GremlinEx to help troubleshoot the more complex key latching use cases.  The scan codes are the keyboard scan codes in hexadecimal that will be listened to to trigger this action.  The "_EX" means the scan code is extended.  This list is important because GremlinEx will only be able to trigger the actions if it "hears" these scan codes in pressed state at the same time.  

Many keys are special - such as the Right Alt key or the numpad keys. For example, the numpad numbers change scan codes based on the state of the numlock key and shift states.

### Numlock state

The keyboard's numlock state alters the hardware codes sent by the numeric keypad (numpad) keys and can in fact caused the keyboard to return the same low level key presses for different physical keys. This happens for example with arrow keys. When this happens, there is no current way in the low level API used to tell which key was pressed because the codes are the same at the hardware level. Because this is usually enabled by the numlock state, Gremlin Ex offers an option as of 13.40.14ex to turn off numlock if it was on when a profile starts.

This does not eliminate the problem entirely as there are still certain key combinations that will report duplicated keys at the hardware level, without GremlinEx able to tell the difference between keys.

If a key combination is not detected, you can use a keyboard scanner to see if the key windows sees is different from what you expect.  There is an option in GremlinEx to display the key scan codes corresponding to a particular key combination, and the keyboard must be able to produce these codes for GremlinEx to act on them.

A free utility to view keyboard scan codes is available [here](https://dennisbabkin.com/kbdkeyinfo)

<!-- TOC --><a name="virtual-keyboard"></a>
### Virtual Keyboard

For input simplicity, GremlinEx now uses a virtual keyboard to show which keys are used for the input selected.  It is still possible to listen to keys using the listen button (currently this will only capture keys, mouse buttons will be ignored).


![](virtual_keyboard.png)



Currently only US layout (QWERTY) is supported for visualization. GremlinEx uses scan-codes (physical keys) on the keyboard so what the key actually says doesn't matter and is only for visualization purposes. I do plan to add localization in a future release so the keys show the correct key name for the current keyboard layout in use.



<!-- TOC --><a name="selecting-a-key"></a>
#### Selecting a key

Click on a key to select it.  More than one key can be selected in most modes. When configuring an input and more than one key is selected, GremlinEx will only trigger the container/actions if all the keys are pressed concurrently.

<!-- TOC --><a name="shift-state"></a>
#### Shift state

If you hold the shift key, keys that can be shifted will show their character.

<!-- TOC --><a name="select-single"></a>
#### Select single

You can select a single key by holding the control key down.  This will clear any other selection.

<!-- TOC --><a name="selected-keys"></a>
#### Selected keys

Each selected key shows highlighted in the virtual keyboard.

<!-- TOC --><a name="listen-button"></a>
#### Listen button

The listen button allows you to type the keys you'd like to select.  This has a limitation in that it will only "hear" the keys that can be pressed.  Listen mode replaces the current selection.

<!-- TOC --><a name="pass-through"></a>
#### Pass-through

Keys uses as inputs into GremlinEx are not captured, meaning that all applications will receive the same keys that GremlinEx sees.

There are no guardrails provided - and GremlinEx does not prevent the output application from seeing the keys and buttons pressed to trigger a GremlinEx action.  When mapping to a game use care to employ key combinations that make sense and do not conflict with one another.

<!-- TOC --><a name="special-considerations"></a>
### Special considerations

Some actions, like mouse wheel presses, do not have a release associated with them (there is no event fired to "stop" the mouse wheel).  When mapping to an output, be aware that the output should be pulsed or otherwise handled if you expect such triggers to be momentary.  For example, if mapping a wheel event to a joystick button, use the pulse mode unless you want the button to stay pressed.

Another potential gotcha is to create a loop, wherein the output of an action creates a trigger for an output.

There are no guardrails to encourage flexibility however it is imperative to use this capability with care to avoid odd behaviors.

<!-- TOC --><a name="midi-device"></a>
## MIDI device

GremlinEx, as of 13.40.14ex, can map MIDI messages and use those to trigger actions.

MIDI is a music oriented protocol to facilitate the exchange of music information between MIDI devices.  These devices can be hardware or software devices.

Unlike hardware devices, MIDI inputs must be user defined and added to tell GremlinEx what to listen to.  Because MIDI can be cryptic, the configuration dialog allows you to listen to MIDI data and automatically program what it "hears" as an input using the listen buttons.  Inputs can also be manually setup if needed.

Gremlin categorizes MIDI messages in that it doesn't look at the value data in the MIDI input stream - rather it looks at the port, the channel, the command, and any specific command data, such as the note number or the controller number.

Gremlin will thus, on purpose, not distinguish between two notes if the velocity is the only thing that changes.  Rather, the MIDI value is passed along to the actions as the value parameter, which enables mapping to joystick values easily (see the trigger mode section below)

<!-- TOC --><a name="midi-inputs"></a>
### MIDI inputs

All MIDI inputs are supported including SysEx messages.  The general process is to add a new input to GremlinEx in the MIDI device tab which will appear on the left.  The input can be configured by click on the cog wheel.

Inputs can be deleted via the trashcan icon, or all inputs cleared via the clear all button.  Use with causion as if you get past the confirmation box, there is no undo and all the container data will be gone unless you previously copied it to the clipboard.  Confirmation boxes only show up if you have a container defined for an input.

<!-- TOC --><a name="midi-trigger-modes"></a>
### MIDI trigger modes

The input has three trigger modes for each MIDI input that alter how the MIDI data is processed by GremlinEx.


| Mode      | Description |
| ----------- | ----------- |
| Change      | Triggers whenever the MIDI value for the current command changes |
| Button      | Triggers a press event if the first argument is in the top half of the MIDI command range, usually 63 to 127.  The trigger value will be shown.   |
| Axis        | The input is placed in axis mode, which enables the vjoy-remap container in axis input mode. The range of the MIDI command value is used, so velocity for a note, value for a CC, etc... |

<!-- TOC --><a name="changing-modes"></a>
### Changing modes

If an input already has mapping containers attached, GremlinEx will prevent switching from an axis mode to a button/change mode and vice versa.  This is because containers and actions, when added to an input, are tailored to the type of input it is, and it's not possible to change it after the fact to avoid mapping problems and odd behaviors.

<!-- TOC --><a name="midi-conflicts"></a>
### MIDI conflicts

MIDI input conflicts are possible and stem from the ability to map MIDI messages via different inputs that map to the same or similar message.   GremlinEx will scan existing mappings to avoid this as much as possible, however it is not foolproof as there are ways to configure MIDI messages in such a way conflicts may not be detected.


<!-- TOC --><a name="midi-ports"></a>
### MIDI ports

GremlinEx listens to all MIDI ports concurrently so multiple MIDI ports can be used at the same time.  GremlinEx will scan for available ports.

If a port goes away after you've configured an input on that port, that port becomes invalid and will not be used for output.  GremlinEx will not delete that input however, but GremlinEx will display a warning on each invalid input.

<!-- TOC --><a name="network-midi"></a>
### Network MIDI

While outside of the scope of this document and GremlinEx, you can easily network MIDI events using [rtpMidi](https://www.tobias-erichsen.de/software/rtpmidi.html).  Another utility that is useful is [loopMidi](https://www.tobias-erichsen.de/software/loopmidi.html). These utilities let you map MIDI input from a device attached to another computer via the network and send that data to the GremlinEx machine.   We won't go into details on how to set that up, but the idea is that a MIDI device sends output to a port, and rtpMidi allows that port data to be transferred to the GremlinEx machine.  GremlinEx will be able to use that input to trigger events.

**important**  GremlinEx will not listen to MIDI data via the remote control feature.  The remote control feature is only for output mapping, not for input.  Use the utilities above to network MIDI traffic which is outside the scope of GremlinEx.


<!-- TOC --><a name="using-midi-from-touch-surfaces"></a>
### Using MIDI from touch surfaces

The MIDI input feature in GremlinEx is designed to work hand in hand with "glass" input surfaces like Hexler's TouchOSC or OSCPilot, or any software based control surface that sends MIDI data.

In TouchOSC's case, if you use the button mode in Gremlin to map a particular command, GremlinEx will press the button while the "glass" button is pressed, and automatically release it when the "glass" button is released.

Similarly, "glass" faders and rotary controls can be mapped using GremlinEx's MIDI axis mode.  Other modes can of course be used if the idea is to trigger an action if a specific range of values are reached.

<!-- TOC --><a name="midi-controllers"></a>
### MIDI controllers

GremlinEx will see any MIDI message so long as the controller shows up as a MIDI port on the machine running GremlinEx (which can be a networked virtual port via rtpMidi).  GremlinEx was tested with hardware from MidiPlus, Arturia, and software controllers like Hexler TouchOSC.  It will also work with any software that outputs MIDI data.

<!-- TOC --><a name="midi-troubleshooting"></a>
### MIDI troubleshooting

The majority of issues will come from messages not being recognized by GremlinEx because the input configuration is causing it to filter (skip) that message.  To this end, Gremlin will tell you what it's listening to.

There are some tools that let you visualize what MIDI messages the computer is receiving such as [MidiOx](http://www.midiox.com/), and older but tried and true MIDI diagnostics tool, or something like [Hexler Protokol](https://hexler.net/protokol).  Both utilities are free.  It's always a good idea to verify the MIDI signaling is functional outside of GremlinEx to verify the machine is seeing messages.  If GremlinEx cannot "listen" to a message via the listen buttons, it cannot see it.


<!-- TOC --><a name="osc-device-open-sound-control"></a>
## OSC device (Open Sound Control)

GremlinEx, as of 13.40.14ex, can map OSC messages and use those to trigger actions.  OSC is generally much easier to setup and program than MIDI.  For more info on OSC, visit 

Unlike hardware devices, OSC inputs must be user defined and added to tell GremlinEx what to listen to. GremlinEx supports any OSC message, although in the current version, limits are imposed on parameter types for ease of processing/mapping to a VJOY device:

OSC messages must consist of a text part, example  /this_is_my_test_fader followed by a numeric value (float or int).   Extra parameters are currently ignored, but can be provided without error.

<!-- TOC --><a name="osc-port"></a>
### OSC port

OSC uses a UDP port to listen on the network for OSC messages.  The default port is 8000 for receiving, and 8001 for sending.   The port can be configured by your OSC utility, just make sure GremlinEx listens on the correct port for messages.  The output port is not used by GremlinEx currently except to configure the OSC client. The output port is always 1 above the input port, so 8001 if the default 8000 input port is used. If you are using a firewall, make sure the port is configured to receive.

The port is configured in options.

The host is auto-configured to the current IP of the machine. Currently, that IP cannot be localhost (127.0.0.1).  This makes sense because any OSC input device will typically run on a separate host, and thus the GremlinEx machine needs to have network connectivity.


<!-- TOC --><a name="osc-inputs"></a>
### OSC inputs

All OSC inputs must be unique or a warning will be triggered in the UI.  An input maps to a specific message type.  In the current release, OSC inputs support the following input modes:

<!-- TOC --><a name="osc-trigger-modes"></a>
#### OSC Trigger modes


| Mode      | Description |
| ----------- | ----------- |
| Change      | Triggers whenever the value changes |
| Button      | Triggers a press event if the first argument is non-zero, and a released event when the first argument is zero  |
| Axis        | The input is placed in axis mode, which enables the vjoy-remap container in axis input mode. A range value can be provided that tells GremlinEx the input range, it can map it to the VJOY range of -1 to +1.  The default is 0 to 1. |


| Command Mode      | Description |
| ----------- | ----------- |
| Message      | The input uses the message (string) part of the OSC message as the input identifier  |

| Message + Data     | The input uses the complete message as the input identifier, including any arguments.    |

The recommendation is to keep it to Message mode as it makes OSC programming much simpler.

A typical OSC command will thus be /my_command_1, number  where number is:

| Value of first argument    | Description |
| ----------- | ----------- |
| range min to range max (usually 0 to 1)    | Axis mapping -1 to +1 |
| zero    | Button release |
| non-zero    | Button press |



<!-- TOC --><a name="changing-modes-1"></a>
### Changing modes

If an input already has mapping containers attached, GremlinEx will prevent switching from an axis mode to a button/change mode and vice versa.  This is because containers and actions, when added to an input, are tailored to the type of input it is, and it's not possible to change it after the fact to avoid mapping problems and odd behaviors.



<!-- TOC --><a name="vjoyremap-action"></a>
# VJoyRemap action 

This mapper is an enhancement to the default remap action. The main enhancements are to show a visual representation of all buttons used, support remote control, eliminate the need to setup many conditions, and to support one-click typical mapping needs directly from the UI.


The VjoyRemap commands are:

| Command      | Description |
| ----------- | ----------- |
| Set Remote Control Only      | Enables broadcast mode and disables local output mode.  In this mode, GremlinEx only sends output to network clients.       |
| Set Local Control Only  | Enables local mode and disables broadcast mode.  In this mode, GremlinEx only sends output to the local machine.         |
| Enable Remote Control      | Enables broadcast mode. This activates broadcast mode regardless of the local output setting. |
| Disable Remote Control      | Disables broadcast mode. This disables broadcast mode regardless of the local output setting. |
| Enable Local Control      | Enables local mode. This activates local output mode regardless of the broadcast output setting. |
| Disable Local Control      | Disables local mode. This disables local output mode regardless of the broadcast output setting. |
| Enable Concurrent Local + Remote Control      | Enables both local and broadcast modes. GremlinEx output goes to both local and remote machines at the same time. |
| Toggle Control      | Inverts current output settings for both local and broadcast controls, whatever they are. |


The commands are only available to button bindings at this time.

<!-- TOC --><a name="vjoyremap-button-press-actions"></a>
## VJoyRemap button press actions


| Command      | Description |
| ----------- | ----------- |
| Button Press     | Outputs a single button to the given VJOY device.  The exec on release option sends the output when the physical button is released.  Start mode sets the output status on profile start.   |
| Button Release | Releases a single button on the given VJOY device.  This is the opposite of press.  This is usually not required but is helpful in some scenarios such as using the tempo container or toggle behaviors.  |
| Pulse     | Outputs a single button to the given VJOY device momentarily.  The default pulse duration is 250 milliseconds, which can be adjusted.  The exec on release option sends the output when the physical button is released.  Start mode sets the output status on profile start.   |
| Toggle     | Toggles (flips) the button output on the given VJOY device. If it was on, it's off, if it was off, it toggles on.  Useful for on/off type activites.    |
| Invert Axis     |  Inverts the specified output axis on the VJOY device.  This flips the direction of output of the axis on the fly by mapping it to a button.  This is specific to games that map the same axis but they are inverted (example in Star Citizen is ship throttle vs vehicle throttle).  When mapped to a physical switch on the throttle, converts from ship mode to vehicle mode for the throttle.  |
| Set Axis Value     | Sets the axis value on the given VJOY axis to a specific value between -1 (min) and +1 (max).  This is useful for detent programming.  |
| Set Axis Range     | Modifies the output range of an axis in VJOY.  The output will be calibrated to the new min/max and has convenience buttons to set half ranges. Use-case: increase sensitivity of physical axis, such as, for landing or roll. |
| Enable remote pairing | When set, the button output locally will also be output remotely regardless of the control mode |
| Disable remote pairing | Turns off remote pairing mode


<!-- TOC --><a name="vjoyremap-axis-mapping-actions"></a>
## VJoyRemap axis mapping actions

| Command      | Description | |
| ----------- | ----------- | ----------- |
| Axis     | Maps source axis to a VJOY output axis. Options:    | |
| | Reverse | Inverts the output of the axis |
| | Absolute | The value of the output matches the raw input value  |
| | Relative | The value of the output is relative to the raw input value  |
| | Start Value | The default axis position on profile start |
| | Scale | Scaling factor applied to the raw input.  Use case: increase sensitivity. |
| | Min/Max Range | Sets the default output min/max range.  The raw input is calibrated to only output between the two values (scale is computed automatically) |

&nbsp;

| Command      | Description |
| ----------- | ----------- |
| Axis To Button     | Maps a raw input range to a specific button.  While the raw input is in that range, the button will be output.  Combine multiples of those to create more than one trigger.  Use-case: detent programming based on axis position.  | |
# Gated axis action

This plugin is an experimental axis input filtering plugin that defines a raw axis input in terms of gates and ranges.  The gated axis plugin combines multiple other features of JGEX and while it's possible to accomplish what the gated axis plugin does, it is often not very simple and has been often the realm of a user-plugin rather than doing it just by plugins, conditions and virtual buttons.

The gated axis plugin is another tool in the toolkit as JGEX can accomplish the same thing different ways - but this can be a much simpler approach to very complex output scenarios in a single action plugin.

It's primary purpose is to easily deal with latching scenarios when the output needs to understand and trigger an action at specific ranges or when crossing certain input values.

The gated axis plugin can only be associated with axis hardware inputs.

![](doc/gate_axis_diagram_1.png)

A gate is a point along the input axis with a specific floating point value in the range -1 to +1.

A range is defined by two gates and are automatically added or removed based on the number of gates.


The gated axis plugin lets you define triggers that can fire when the input axis is either crossing a gate, or within the bounds of a range between two gates.

These actions are configured as sub-containers of the action.  Each gate or range has its own set of configured triggers accessible via the configure button.

The top visual is a horizontal representation of the input axis and the configured gates and ranges on it.   The lowest value is on the left, the highest is on the right.

## Gates

A gate is a point along the axis and has a unique floating point value.


Gates are always organized from lowest to highest, and as gates are added, they are always re-ordered in sequence.

Gates cannot overlap.

At least two gates must be defined.

When gates are added or removed, the gates are always re-ordered in linear fashion from smallest to highest.

Gates can be added by specifying the number of gates you would like and pressing the "set" button (this also removes gates if needed).

A gate can be added by right clicking any range without a gate.

A gate can also be added by moving the input hardware to the desired location and clicking the add button (noting that a gate cannot be added on top of another gate).

The value of a gate can be changed by dragging the gate to a new location, or manually entering the numeric value for that gate, or moving the input the new desired location and clicking the record button for that gate.


Each gate has a configuration panel that allows you to add one or more actions JGEX should take whenever the input axis value crosses the gate.  The configuration panel allows you to add containers and action to the gate, just like you can add containers and actions to input hardware.  The difference is that the actions and containers will use filtered data based on the gated axis, and not the raw input data.

The configuration panel can be opened by clicking the configure button for that gate, or right-clicking the gate itself (be sure to click on the gate as if you right click on the range it will add a new gate there).

Gate can be deleted by clicking the delete button for each gate, or clicking the delete button on the gate's configure panel, or by reducing the number of gates (set button).  A deleted gate will also delete its configuration including any configured actions, and deletions needs to be confirmed as it can result in data loss.

Gate crossings can be bidirectional (the value crosses the gate in either direction), or directional (the value crosses the grate as it increases, or decreases).  The directional feature is used when you need to trigger an action when entering or exiting a range, but not both.  The bidirectional feature is the default, and will trigger whenever the input value crosses the gate.

Gates are triggered once so if the input does not change and sits on a gate, the gate will only trigger once.  Another way to put this is a gate will only trigger if the input changes.


| Condition      | Description |
| ----------- | ----------- |
| Cross | The gate will trigger whenever the input crosses the gate |
| Cross (inc) | The gate will trigger if the gate is crossed from left to right, or in increasing value |
| Cross (dec) | The gate will trigger if the gate is crossed from right to left, or decreasing value |


A gate can be edited by right clicking on a gate or by clicking the configuration (gear) button for that gate.

A gate value can be set by dragging the gate on the control, or by manually entering the data on the input for that gate using a floating point value in the range -1 to +1.



The recommended workflow is to define the gates you want first, then add configurations to them.  This is because when you add or remove gates, while JGEX will do its best to keep configurations saved for removed gates and restore them later, as you add/remove gates, the gate order may change so the actions defined for that gate may no longer be the right gate (an example of this is - you inserted a gate between two other gates).  Of course you can use the copy/paste action between gate configurations.   This will result is a lot less editing.  What I'm saying is that if you delete a gate, it will likely delete the config for that gate, so if you decided you wanted the gate after-all and re-add it, you'll need to reconfigure the gate.  JGEX will confirm deletions.

### Gate Delay

The delay is a value in milliseconds that determines how much time elapses between a press and release action.  Internally a gate will mimic a button press, so will send two specific events to sub-actions on a gate, a press action, followed by a release action.  Setting this to zero means the two are instant.  The default value is 250 milliseconds (1/4 second) which is enough time for most games to capture the input, either a keyboard press or a button press.

### Gate Actions

Gate containers and actions will see the input as a joystick button.  The value of the button should not be used by the action because the trigger will occur whenever the gate is crossed and the hardware input button will always be the same for all gates.

However each gate keeps it own set of containers of actions for that gate only - the configuration is not shared by multiple gates.

A gate that has no containers defined is just ignored.


## Ranges

A range is defined by the area between two gates.  A range has modes that define the behavior of the output value when the input is in that range:

| Mode      | Description |
| ----------- | ----------- |
| Normal | The value is output as is (this is the default) |
| Fixed | The value is set to a constant output - this value will be output whenever the input is this range |
| Ranged | The value is scaled to the range's defined minimum and maximum - this mode allows you to scale the output to a new set of values |
| Filtered Out | No value is output in this mode - use this to prevent a value from being output whenever the input is in the range |


Ranges cannot overlap (one exception - the default range).

Whenever you add or remove gates, ranges are added or removed as well.  It is recommended you don't configure ranges until you have the number of gates finalized to avoid inadvertently loosing configured actions because a range was deleted as you removed a gate.  JGEX will confirm deletions.

### Default range

The default range is a special range that is used for how the gated output should behave when the input is not in configured range.   A configured range is a range that has actions and modes defined. The default range is used when a range exists, but is not configured to do something special.

You can use the default range to your advantage by only configuring special ranges in the input axis - and let the default range handle what happens when the input is not in the special ranges you've defined.

### Range actions

Containers and actions added to a range will see the input as an axis.

A range without defined containers is ignored and will use the settings of the default range (if default actions are defined).

## Use-cases and scenarios for gated output

The gated axis plugin can be useful for a number of scenarios where more sophistication is needed on input axis data.

The plugin can be used for complex axis to button mapping, for establishing complex setups for latched output, and for scaling purposes.

A use-case for this is to exclude a specific input range from the output.  In this scenario, you'd define the default output using the default range, and only configure the special range to override the default that turn the output off whenever the input is in a given range. This is helpful to fix a value or prevent a value from being output at specific points on the input axis, also known as latches or deadzones.

For example you can setup a filter range if your input flutters to prevent it from being output. To setup a deadzone at the latch point on the axis, for example the middle.  You can define a small range near the middle of the axis and set it to not output any value.  You can then setup the two side ranges to "range" the output so that you still get the full range of output values, but you have a deadzone where the middle range is concerned.

A gate can be configured to send an action when it is crossed, for example, entering beta mode on a turbo-prop throttle, or activating engine reversers.   The gate mechanism is very helpful to map to simulators that have gated throttles as it becomes easy to send the appropriate values and commands as the input lever is moved.

The gated axis can be setup to send two different axes based on two (or more) ranges, including inverting ranges or sub-scaling them.



<!-- TOC --><a name="map-to-mouse-ex-action"></a>
# Map to mouse EX action

This plugin is identical to the Map to Mouse plugin but adds a wiggle function, easy execute on release and button hold functionality. When wiggle is enabled, the mouse will move slightly by itself every 10 to 40 seconds and move back.  It will do that until wiggle mode is turned off.  
  
The purpose of wiggle is to keep an application alive.   Wiggle is turned on/off separately for remote/local clients.

| Command      | Description |
| ----------- | ----------- |
| Mouse Button | Outputs one of the mouse buttons |
| Mouse Axis | Moves the mouse |
| Wiggle Enable (local) | Jolts the mouse every few seconds  |
| Wiggle Disable (local) | Stops the mouse wiggling if it was turned on.  |
| Wiggle Enable (remote) | Jolts the mouse every few seconds on remote clients  |
| Wiggle Disable (remote) | Stops the mouse wiggling if it was turned on for remote clients  |


Mouse commands can forced to be sent to remote hosts only, or to send them concurrently to the remote host regardless of the remote control state.


<!-- TOC --><a name="map-to-keyboard-ex-action"></a>
# Map to keyboard EX action

This is identical to the base keyboard mapper but adds a few functions I thought would be handy.

The updated keyboard mapper adds separate press (make), release (break) functionality so keys can stay pressed, or just released separately.

It also adds a delay (pulse) function to hold a key down for a preset period of time (default is 250 milliseconds or 1/4 of a second which is the typical game "detect" range as some games cannot detect key presses under 250ms in my experience.

The make/break/pulse behavior applies to all keys in the action, and the keys are released in the reverse order they were pressed.



<!-- TOC --><a name="dragons"></a>
### Dragons

This action is an experimental feature.

Make sure that if you use a press action, there is a companion release action somewhere.  If that doesn't happen, you can press the key on your keyboard and it will release the key.

When a key is pulsed, the release will occur regardless of input state or conditions.



<!-- TOC --><a name="range-container"></a>
# Range container

The range container is a container designed to break up an axis input ranges into  one or more actions tied to a particular range.  While something like this can be done with conditions, the range container is much easier to setup than using conditions. 

The idea of a range container is to setup a range of axis values that will trigger one or more actions.   As many actions as needed can be added.  An example of this is mapping a flaps axis to distinct keys, or setting up button presses based on the value of an input axis, which is helpful for example, for throttle setups on some flight simulators to setup detents.

The range container has a minimum and a maximum and each boundary and be included or excluded to define the range.

There is a convenience button that will create automatic ranges to an axis: you specify how many axis "brackets" you need, and you can give it a default action.  This will create range containers for the axis automatically and compute the correct bracket values for the count provided.

The Add button adds containers.  The add and replace button replaces all the range containers with the new range value (use with care as it will blitz any prior range containers).

The range container is designed to work with joystick buttons or the enhanced keyboard mapper (map to keyboard ex)

<!-- TOC --><a name="ranges"></a>
### Ranges

All joystick axis values in JGex are -1.0 to +1.0 regardless of the device, with 0.0 being the center position.

<!-- TOC --><a name="includeexclude-flag"></a>
### Include/exclude flag

Each bracket can include or exclude the value.  Think of it as greater than, versus greater or equal to.   This is use to include or exclude the boundary value when JGex is determining if the action should trigger or not.

<!-- TOC --><a name="symmetry"></a>
### Symmetry

The symmetry option applies the opposite bracket as the trigger.  So if the bracket is (0.9 to 1.0), in symmetry mode the bracket (-1, -0.9) will also trigger if the axis is in that range.


<!-- TOC --><a name="latching"></a>
### Latching

The range container is latched - meaning that this special container is aware of other range containers in the execution graph.  The latching is automatic and ensures that when the axis is moved to a different position, prior active ranges reset so can re-trigger when the axis moves into their range again, so the container has to be aware of other ranges.

<!-- TOC --><a name="dragons-1"></a>
### Dragons

This container is an experimental feature.

The range mapper is not designed to work with the default keyboard mapper as that will cause stuck keys, because of how the default keyboard mapper works when conditions are not used.  Use the enhanced keyboard mapper.

The latching feature (awareness of other range containers) may introduce some strange behaviors and applies to all ranges attached to a single axis, so it's not aware of nesting for example.  The latching applies to all ranges in the mapping tree regardless of their level.

<!-- TOC --><a name="button-container"></a>
# Button Container

This experimental container simplifies the mapping of actions when an input button is pressed or released.  While this can be done with conditions, this is a simpler and easier way to map a button to a set of actions when a button is pressed or released.

<!-- TOC --><a name="usage-tips"></a>
### Usage tips

This container is best used to handle an on/off function (the input only triggers when in one of two possible positions), or a three way function (the input triggers in two out of three positions - the middle position usually being the one that doesn't trigger)

<!-- TOC --><a name="pressed-block"></a>
### Pressed block

In this section, add the container or actions you want to execute on button press.  Leave blank for no action.

<!-- TOC --><a name="release-block"></a>
### Release block

In this section, add the container of actions you want to execute on button release.  Leave blank for no action.

<!-- TOC --><a name="tempoex-container-tempo-with-chain"></a>
# TempoEx Container (tempo with chain)

This experimental container combines the Tempo and Chain containers together.  The container has two main sections, a short press action set, and a long press action set.  The delay box indicates how long the (real) button has to be held before selecting either a short or long set.

Each action set contains one or more chain groups.

Each chain group contains one or more actions.  A group will execute all the actions in that group.

Chaining means that at every short press, or long press, the container will sequence through the chain groups for that action set in round robin fashion.

The chaining behavior can be prevented if needed (although that's really the point of the container).

The chain delay is included although it will conflict with long press.  I may remove it later because the value may be limited in most use-cases that would benefit from this container.

Within each action set, the chain group entries can be re-ordered, or can be removed.




<!-- TOC --><a name="plugin-script-enhancements"></a>
# Plugin Script enhancements
 

GremlinEx adds a few custom Gremlin script decorators to facilitate custom scripting and control from Python.

<!-- TOC --><a name="gremlininput_devicesgremlin_start"></a>
### @gremlin.input_devices.gremlin_start

Called when a profile is started - lets a script to initialization when a profile starts to run

<!-- TOC --><a name="gremlininput_devicesgremlin_stop"></a>
### @gremlin.input_devices.gremlin_stop

Called when a profile is stopped - lets a script cleanup when the profile stops running

<!-- TOC --><a name="gremlininput_devicesgremlin_mode"></a>
### @gremlin.input_devices.gremlin_mode

Called when the mode is changed (use def mode_change(mode) - mode will be a string) - lets a script get a notification when there is a profile mode change somewhere in GremlinEx.


<!-- TOC --><a name="gremlininput_devicesgremlin_state"></a>
### @gremlin.input_devices.gremlin_state

Called when the state information is changed (local, remote or broadcast mode). The event properties is_local, is_remote and is_broadcast are flags that contain the current state of GremlinEx.


<!-- TOC --><a name="recipes"></a>
# Recipes

<!-- TOC --><a name="one-way-or-two-way-switch-to-two-way-switch-three-way-switch"></a>
## One way or two way switch to two way switch / three way switch

Some hardware controllers only have a trigger on one (two) positions out of two (three).  Usually the center doesn't have a button mapped.  

In GremlinEx VjoyRemap a button trigger can easily be output for each position of a switch by adding a release mapping to the hardware positions that do trigger on.  The trigger occurs then when the switch leaves the position and turns off.

One responds to button presses on the raw hardware, the other responds to a button release on the raw hardware.

| Mapping     | Description |
| ----------- | ----------- |
| Send VJOY output   | Sends a button press to VJOY device and button when the position of the button is active.      |
| Send VJOY output (on release)   | Sends a button press to VJOY device and button when the position of the button is no longer active.  The checkbox "execute on release" is selected in this case.  |

The equivalent pulse commands can be send to send a momentary pulse rather than having the button on all the time if that is needed.

<!-- TOC --><a name="longshort-press-buttons-or-keyboard"></a>
## Long/short press - buttons or keyboard

You'll use the tempo container sets up two action blocks, one for short press, the other for long press.  The tempo container lets you select a long press delay, so if the input is held long enough, the long action is triggered.

The relevant behaviors of the Vjoyremap action are Button Press, Button Release and Toggle.

Note: this applies to keyboard actions as well, and you can just as easily use this for keyboard presses using the enhanced keyboard action's ability to separate out key presses from key releases.

<!-- TOC --><a name="to-setup-concurrent-button-presses-hold-the-short-press-while-long-press-is-active"></a>
### To setup concurrent button presses (hold the short press while long press is active)

In this scenario, both outputs will be active if the input button is held long enough to trigger the long press.

The vjoyremap action in the short action block should be set to *button press*.  The vjoyremap action in the long action block should also be set to *button press*.  The resulting behavior is the short and long buttons will both be pressed if the input button is held long enough, and both will release when the input is released.


| Mapping     | Description |
| ----------- | ----------- |
| Short action block   | VjoyRemap set to *button press* and/or MaptoKeyboardEx set to "press" for the output on short hold      |
| Long action block   | VjoyRemap set to *button press* and/or MaptoKeyboardEx set to "press" for the output on long hold |


<!-- TOC --><a name="to-setup-a-latched-short-then-long-button-press-with-only-one-button-active"></a>
### To setup a latched short, then long button press with only one button active

In this scenario, either short or long will be active if the input button is held long enough to trigger the long action.  If you hold the input long enough, the short button will release, and the long button will stay pressed as long as you hold the input.  Only one button will be output at a time.

Add a vjoyremap in the short action block set to *button press*.

Add two vjoyremaps in the long action block.  The first will map to the long press output button and the mode is set to *button press*.

The second vjoyremap will be set to *button release* and map to the same output button in the short action block. 

| Mapping     | Description |
| ----------- | ----------- |
| Short action block   | VjoyRemap set to *button press* and/or MaptoKeyboardEx set to "press" for the output on short hold      |
| Long action block   | VjoyRemap #1 set to *button press* and/or MaptoKeyboardEx set to "press" for the output on long hold |
| Long action block   | VjoyRemap #2 set to *button release* and/or MaptoKeyboardEx set to *release* to release the short press action |


<!-- TOC --><a name="scripting-logic"></a>
## Scripting logic

Any logic that depends on reading more than one hardware value is best done as a plugin.  Plugins are Python files "attached" to a GremlinEx profile and the script enhancements make it possible to run a function when a hardware event occurs.

<!-- TOC --><a name="attaching-a-function-to-a-hardware-event"></a>
### Attaching a function to a hardware event

You use a Python decorator to map a function to a hardware event.  The decorator starts with the @ sign and tells GremlinEx what hardware and input you are mapping to.

GremlinEx adds a Script Generator button to the Device Information dialog that copies all current hardware device names, IDs and automatically creates decorators out of them that can be pasted directly into a Python script file.



<!-- TOC --><a name="recommended-resources"></a>
## Recommended Resources

<!-- TOC --><a name="vjoy-virtual-joystick-driver"></a>
#### VJOY virtual joystick driver 
 
https://github.com/shauleiz/vJoy

Installs one or more virtual programmable HID joysticks on Windows with up to 8 axes, 4 hats and 128 buttons per the DirectInput specification.

<!-- TOC --><a name="osc-support-in-joystick-gremlin-from-touchosc"></a>
#### OSC support in Joystick Gremlin from TouchOSC

https://github.com/muchimi/TouchOsc

Transforms any touch screen into a game control surface, similar to GameGlass.


<!-- TOC --><a name="hidhide"></a>
#### HIDHIDE

This tool hides raw hardware only exposing the VJOY devices.  Essential to not confuse games or simulators.

https://github.com/nefarius/HidHide

<!-- TOC --><a name="hexler-touchosc"></a>
#### Hexler TouchOSC

A touch enabled surface designer initially setup for the OSC (open sound control) and MIDI protocols to control musical instruments, DAWs and live performances.  Supports multiple platforms.  Has a free version but the license is well worth the price.  Simple set of controls, but very powerful because of the available LUA based scripting and works on any platform, thus making your phone, tablet or touch-enabled desktop function as an input device.

https://hexler.net/touchosc#_

I also recommend the Protokol tool to diagnose any OSC issues.



<!-- TOC --><a name="troubleshooting-guide"></a>
# Troubleshooting guide 

<!-- TOC --><a name="hid-devices-detection-random-disconnects"></a>
## HID devices - detection / random disconnects

Random disconnections of HID devices or not detecting devices are typically caused by these root causes in my experience, these are unrelated to GremlinEx:

	(1) total cable is too long or faulty - test a different cable - use a cable 1.5m/ 5' max and match the cable to the device type (blue connectors for USB 3.0, white connectors for USB 2.0).  You can connect a 2.0 device to a 3.0 hub using a 2.0 cable.  Don't use a 2.0 rated cable for a 3.0 controller.
	(2) cable/connection (at either end) - this is usually a connector not plugged in completely, or the connection is worn out or bent.
	(3) insufficient power provided to the USB device - this is frequent especially if using older USB Hubs - use a good quality powered USB hub if you have more than one device, and some cheaper hubs are unable to provide full spec power (5 volt at 0.5A to 0.9A) - half an amp for USB 2.0 devices, 0.9A for USB 3.0 devices, per port.  Do not use un-powered hubs.
	(4) Windows is configured by default to turn off power to USB devices after some time - and it doesn't always detect when a controller is in use. Disable USB power management in Windows (this is usually done via device manager but there are articles online how to do this). NOTE: major Microsoft patches can re-install drivers and reset to default - so you may have to check power settings after some patches.
	(5) machine was not cold started after a USB device was connected/disconnected. The theory is - yes - you can hot-connect or disconnect USB devices - and it "should" work. If you run into an issue - the first thing to do is to reboot the machine after you've made the modification, and to be extra sure on my end, I cold start to make sure all is re-initialized, including the BIOS and the hardware so the next bootup sequence is going to be predictable. I have some older devices (CH was notorious for this) causing all sorts of headaches because the "logic" was not in the hardware but in some software drivers they had. A telltale sign is if your controller comes with driver software to make it work. Rebooting may be an extra step but it can save a lot of headaches. I found the most problem-free joystick/wheel/pedal controllers are those that are detected as generic HID devices without the need to run any software that came with the device and they are visible to windows (when HIDHide is not enabled) to the control panel app joy.cpl
	(6) if using a wireless USB device - make sure the batteries are ok. I don't recommend using wireless devices for anything but a mouse or a headset - neither is going to be used by GremlinEx. Wireless is convenient but can also be a source of headaches for game controllers.
	
	
<!-- TOC --><a name="hid-troubleshooting-tips"></a>
## HID troubleshooting tips 

Your HID devices should function without GremlinEx installed and be stable using whatever tools came with them to diagnose/test them. Just make sure that HIDHide is not hiding the devices from these utilities when testing. If the HID devices are not stable in Windows - they won't be in GremlinEx either.

If your HID device starts acting up - use a process of elimination and change one thing at a time until you find the root cause. If you change multiple things, like connection, hub, number of devices, multiple changes will make it more difficut to diagnose the issue.

Some tests you can attempt to see if it makes a difference (and yes, it can be tedious to do but necessary in some cases):

- disconnect other devices so you only have one to test. Add devices progressively to make sure there is no conflict between devices.

- change the wire in case the wire / connections are the issue.

- change the port the hub or device is connected to

- connect direct to the computer or a different hub

- make sure your hub is able to deliver the spec power to each port (some come with power supplies that cannot do this)

- Use a USB 2.0 hub for controllers that are USB 2.0 as I've run into some problems sometimes with USB 3.0 hubs (the older models in particular) - I think there was a chipset issue with a whole series of those that caused translation issues - hence why try a different hub to see if it works - the older the controller the more important that is (like CH products and some older Logitech / Microsoft devices).

- If the device came with firmware (example Virpil. Thrustmaster, VKB, MTG...) - make sure you're running the current firmware.

- With HIDHide disabled (not hiding devices), run a command line (windows key + R), type joy.cpl and make sure your controller is seen by Windows. Don't calibrate - in the test button, your controller axes and buttons should move and respond. This app makes sure that Windows sees the devices correctly - this must happen before GremlinEx can see them.

- If you connect/disconnect controllers like joysticks, wheels, pedals - anything with an axis or button that isn't a keyboard type device - windows will invariably re-order these things. A reboot will usually get you the final order of things, but the order can change whenever you add or remove one of these devices. In general, if you have to constantly connect/disconnect devices, look into using profiles and ways for you not constantly to have to connect/disconnect devices. Doing this can wear out the connectors. Also, it's really asking for trouble because you are effectively making a hardware change every time you do this. Should it work? Absolutely. The question is more about how much you value your sanity and like doing troubleshooting. Avoid disconnecting/reconnecting things if you can, and I get it's not always possible. My experience with HID controllers, especially if you have a lot of them, is set it up once, and then it will work all the time.


<!-- TOC --><a name="hidhide-troubleshooting"></a>
## HIDHide troubleshooting

HIDHide is a key layer that hides the raw hardware that you are mapping to a game to VJOY via GremlinEx.

HIDHide prevents conflicts in games when the raw hardware is visible to the game, at the same time the virtual (vjoy) hardware is. This can cause many different problems - from the game not detecting the right input - to things not being detected at all to very strange behaviors.

HIDHide is very stable in my experience but you need to run it and verify the configuration ***every time you connect or disconnect hardware*** (which is one reason to please figure out a way to not constantly connect/disconnect).

How can you tell HIDHide is working or not? Use joy.cpl - the windows control panel joystick app from 25 years ago, and it should only "see" the devices you can the game to see. If you see all your raw hardware - HIDHide isn't doing its job.

What does it look like when HIDHIde is set up correctly? vjoy.cpl only shows your VJOY devices, all your actual "raw" controllers will not work there.

<!-- TOC --><a name="checking-your-mappings"></a>
## Checking your mappings

Vjoy comes with an excellent Vjoymonitor utility that will display what outputs you have. Test your scripts and Vjoy output before you jump in the game to make sure that all looks good there.  

That will show all your vjoy devices and let you verify the mapping is as expected. I use it constantly to check inversion and button pulse vs hold mappings. If vjoymonitor doesn't show what you expect, it will definitely not work correctly in the game either.

Note: this will not show if the raw hardware is properly hidden.  For this, use joy.cpl as indicated above as that shows what Windows sees (thus what your game will see).

In nearly all cases - what I found usually happens:
- HIDHide isn't hiding the raw devices (run it and check its configuration)
- GremlinEx isn't running the profile
- there's some sort of hardware issue and confusion linked to disconnect/reconnect
- you're using a controller that isn't a DirectInput HID game controller as classified by windows - so a device with axis/button definitions  - this happens a lot with gamepads although most can be setup as a regular (non gamepad) controller.

<!-- TOC --><a name="gremlinex-has-been-tested-with"></a>
## GremlinEx has been tested with 
- Virpil
- Thrustmaster
- MTG
- Logitech
- Honeycomb
- Microsoft
- Arduino (with HID library)
- RasberryPi (with HID library)
- TouchOSC
- StreamDeck (via vjoy plugin and OSC plugin)
- AxisAndOhs


<!-- TOC --><a name="sample-scripts"></a>
## Sample scripts

I'm including some of my Python scripts for GremlinEx as reference because these are my primary way to do advanced mapping when the UI elements are limited, including one that handles OSC inputs.  The comments are in the files.

These are provided as-is as an example of advanced scripting you can do in GremlinEx.  I personally find scripting significantly faster than attempting to do this via the UI for complex mappings, especially when I start getting into release behaviors or latched behaviors for complex simulation software.

The example scripts do things like combining axes together, latching (so one button or axis value on one controller impacts the behavior of another), scaling an axis, curving an axis, text to speech, sending keyboard and mouse output from a script, how to access the raw value from a device, do some basic math and state mapping outside of profile modes, handling OSC (Open Sound Control) messages, etc...  

The scripts use specific enhancements to Gremlin so have additional decorators to expose internal events in Gremlin such as profile start/stop so the script can initialize or cleanup.

These won't run as they are in your system because your devices and hardware IDs will be different from mine, but that's all setup in the config.py file.   You can get your hardware IDs by running GremlinEx and viewing the device list which will have the information you need to plugin config.py for your particular config.

This is a very advanced topic, talking about dragons, and assumes you have a good understanding of Python and how GremlinEx works.  The examples are well commented so hopefully self-explanatory.

Scripts are attached to a profile using the scripting tab in GremlinEx.  You do not need to reference config or util - only the main script (dependencies will load).  Make sure all the files are in the same folder as your profile XML files.

Note: because of how Python works, if you change dependencies like config.py or util.py, you have to close down GremlinEx and reload it.  You can change the script .py and start the profile without having to exit as long as the script dependencies don't change.

The sample scripts includes one for Star Citizen, Microsoft Flight Simulator and OSC.

<!-- TOC --><a name="osc-open-stage-control-info"></a>
## OSC (open stage control) info

OSC is a topic by itself, and if you're wondering what this has to do with gaming and controllers, OSC is heavily used in the music industry to drive touch surfaces like a tablet, phone or a touchscreen (connected to a different box from your main gaming machine), and send commands to music software (usually a DAW or VST) or live on-stage equipment including things like stage lights.  

I'm using the same concept to take OSC messages in GremlinEx, which are nothing more but text (string) messages and values, and duplicate functionality found in tools like GameGlass or some other game specific controls using OSC software to send input to games.  OSC is very powerful and customizable, and because OSC knows about faders and buttons and touch surfaces, it becomes easy to map to an axis, buttons, and do sophisticated things like 2D touch surface for shield mapping for example.  Very powerful indeed.

If you use the OSC plugins for StreamDeck or LoupeDeck, it enables these more esoteric devices to be used by GremlinEx, and the networking function means that these devices can be used anywhere on your local network so they don't need to be attached to your local gaming computer.


<!-- TOC --><a name="python-dependencies"></a>
## Python dependencies

If you want to run from the source code, you will need the following python packages for the 64 bit version of python your are running (3.11+)

	pyside6
	pywin32
	msgpack
	reportlab
	dill
	mido
	python-rtpmidi
	lxml


