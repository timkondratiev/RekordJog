import mido

def tempo_reverse(ims, midi_out, PIONEER_PITCH_CONTROL):
    if ims.control == 0x08:
        inverted_value = 127 - ims.value
        midi_out.send(mido.Message('control_change', control=PIONEER_PITCH_CONTROL, value=inverted_value, channel=ims.channel))
