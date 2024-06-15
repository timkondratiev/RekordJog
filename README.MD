# RekordJog: a translator from third-party controllers to Rekordbox.

## Description

This program allows jog wheels and pitch control on third-party controllers to work in Rekordbox 6 and 7. Currently, it is optimized for the Allen & Heath Xone:4D. To use it with other controllers, you'll need to modify and optimize the source code. I may make this program universal in the future if there is enough interest.

Please note that a paid subscription for AlphaTheta (Pioneer) Rekordbox 6 is required for this program to run properly.

## Installation

1. Clone the repository and open the directory in Terminal.
2. Create a virtual environment:
```bash
python3 -m venv .venv
```
3. Activate the virtual environment:
```bash
source .venv/bin/activate
```
4. Install requirements:
```bash
pip3 install -r requirements.txt
```
## Usage

1. Make sure the controller is connected and recognised by the system by running:
```bash
python3 checkForMidiDevices.py
```
2. Launch the app in Terminal:
```bash
python3 app.py
```
3. Open Rekordbox.
4. (Optional) Import MIDI mapping for your controller from `controller_mapping` directory. Everything should work now.
5. When the DJ session is over, stop the app by pressing `Ctrl+C` in the Terminal where the app was launched.

## MIDI mappings

### Allen & Heath Xone:4D

For better precision, 2 faders are used for each deck pitch control. 2-nd fader increments smaller values.

## How to map jog wheels

First, you need to figure out what MIDI message is sent on your jog turn. Then analyze which values are sent at different rotation speed.

In my controller, the jogs send values between 1 and 30 clockwise and between 127 and 98 counter clockwise. Notice that the total number of possible values is limited and there was a noticeable gap between them, you can see all possible values and what I mapped them to in code below:

```
CONV_J_VAL = {
    1:65,
    2:66,
    4:67,
    7:69,
    11:71,
    16:73,
    20:75,
    30:80,
    
    127:63,
    126:62,
    124:61,
    121:59,
    117:57,
    112:55,
    108:53,
    98:48
    }
```

As you can see from this mapping, rekordbox expects neutral value to be 64 (although it is never used), and this value is increased for CW rotation and decreased for CCW rotation. The scale is also different, so for the value of 30 I add 16 to the neutral position.

I used this article as a reference. There is a lot of useful information. https://djtechtools.com/2017/05/08/hack-rekordbox-use-controllers-jogwheels/

And also these resources were handy:

Pioneer DDJ-SX reference for MIDI mapping: https://www.pioneerdj.com/-/media/pioneerdj/software-info/controller/ddj-sx/ddj-sx_list_of_midi_messages_e.pdf 

You can also find Pioneer DDJ-SX MIDI mapping in Rekordbox source files. For mac the file is at: `/Applications/rekordbox 6/rekordbox.app/Contents/Resources/MidiMappings/PIONEER DDJ-SX.midi.csv`

Hex to decimal converter: https://www.rapidtables.com/convert/number/hex-to-decimal.html

MIDI messages reference: https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes

https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
