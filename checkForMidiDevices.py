# Import mido library
import mido

# Print all available MIDI input ports
print("Available MIDI input ports:")
for port in mido.get_input_names():
    print(port)

# Print all available MIDI output ports
print("\nAvailable MIDI output ports:")
for port in mido.get_output_names():
    print(port)
