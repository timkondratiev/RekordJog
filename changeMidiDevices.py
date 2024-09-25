from functions.set_midi_devices import set_midi_devices
try:
    set_midi_devices()
except KeyboardInterrupt:
    print("\nExiting, bye.")