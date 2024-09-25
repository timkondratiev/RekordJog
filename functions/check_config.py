import configparser
import mido
from functions.set_midi_devices import set_midi_devices

def check_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'MIDI' in config:
        midi_inp = config['MIDI'].get('input_device')
        midi_out = config['MIDI'].get('output_device')
        return midi_inp, midi_out
    else:
        midi_inp, midi_out = set_midi_devices()
        return midi_inp, midi_out