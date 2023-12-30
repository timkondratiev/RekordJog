# RekordJog: a translator from third-party controllers to Rekordbox.

## Description

This program allows jog wheels and pitch control on third-party controllers to function with Rekordbox 6. Currently, it is optimized for the Allen & Heath Xone:4D. To use it with other controllers, you'll need to modify and optimize the source code. I may make this program universal in the future if there is enough interest.

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

1. Make sure the controller is connected and recognised by the system.
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
