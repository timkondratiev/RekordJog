import mido

from functions.check_config import check_config
from functions.jog_incremental import jog_incremental
from functions.rekordjog_start_sequence import rekordjog_start_sequence
from functions.tempo_reverse import tempo_reverse

TURN_CLOCK_SPEED = 0x46
TURN_COUNTER_SPEED = 0x3A
JOG_SIDE_CODE = 0x09
JOG_TOP_CODE = 0x0a
PIONEER_PITCH_CONTROL = 0x70

def main():
    midi_inp, midi_out = check_config()
    try:
        with mido.open_input(midi_inp) as midi_inp, mido.open_output(midi_out) as midi_out:
            rekordjog_start_sequence()
            wheel_messages_counter = 3
            while True:
                ims = midi_inp.receive()
                if ims.type == 'control_change':
                    wheel_messages_counter = jog_incremental(ims, midi_out, wheel_messages_counter, TURN_CLOCK_SPEED, TURN_COUNTER_SPEED, JOG_SIDE_CODE, JOG_TOP_CODE)
                    tempo_reverse(ims, midi_out, PIONEER_PITCH_CONTROL)

                if ims.type == 'note_on' or ims.type == 'note_off':
                    midi_out.send(mido.Message(ims.type, channel=ims.channel, note=ims.note, velocity=ims.velocity))
    except KeyboardInterrupt:
        print("\nClosing RekordJog, bye.")

if __name__ == "__main__":
    main()
