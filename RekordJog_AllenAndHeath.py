import mido
import math
from functions.check_config import check_config
from functions.rekordjog_start_sequence import rekordjog_start_sequence


# The JOG_MULTIPLIER is required for smooth jog operation. 
# Pioneer controllers seem to be sending MIDI signal at a much higher rate than XONE:4D. 
# If you send one fake Pioneer message for each Xone jog message, scratching sounds unnatural.
# You need to test different values for other controllers.
JOG_MULTIPLIER = 15 

CONV_J_VAL = {
    1:65,   #0
    2:66,   #1
    4:67,   #1
    7:69,   #2
    11:71,  #2
    16:73,  #2
    20:75,  #2
    30:80,  #5
    
    127:63,
    126:62,
    124:61,
    121:59,
    117:57,
    112:55,
    108:53,
    98:48
    }

tempo_values = [
    [63, 63],
    [63, 63],
    [63, 63],
    [63, 63],
]

JOG_CODES = [
    [0xBF, 0x25],
    [0xBF, 0x2D],
    [0xBE, 0x25],
    [0xBE, 0x2D],
]



TOUCH_ON_CODES = [
    [0x9F, 0x26],
    [0x9F, 0x46],    
    [0x9E, 0x26],
    [0x9E, 0x46],
]

TOUCH_OFF_CODES = [
    [0x8F, 0x26],
    [0x8F, 0x46],    
    [0x8E, 0x26],
    [0x8E, 0x46],
]



TEMPO_BIG_CODES = [
    [0xbf, 0x11],
    [0xbe, 0x11],
    [0xbf, 0x1f],
    [0xbe, 0x1f],
    [0xbf, 0x13],
    [0xbe, 0x13],
    [0xbf, 0x1d],
    [0xbe, 0x1d],
]


TEMPO_SMALL_CODES = [
    [0xbf, 0x10],
    [0xbe, 0x10],
    [0xbf, 0x1e],
    [0xbe, 0x1e],
    [0xbf, 0x12],
    [0xbe, 0x12],
    [0xbf, 0x1c],
    [0xbe, 0x1c],
]

def jog(msg):
    id = JOG_CODES.index(msg.bytes()[:2])
    v = CONV_J_VAL[msg.bytes()[2]]

    ms = mido.Message.from_bytes([176+id, 0x22, v])

    for i in range(JOG_MULTIPLIER):
        midi_out.send(ms)

def tempo(id):
    msb = mido.Message.from_bytes([0xB0+id, 0x00, tempo_values[id][0]])
    lsb = mido.Message.from_bytes([0xB0+id, 0x20, tempo_values[id][1]])
    midi_out.send(msb)
    midi_out.send(lsb)

def main():
    midi_inp, midi_out = check_config()
    try:
        with mido.open_input(midi_inp) as midi_inp, mido.open_output(midi_out) as midi_out:
            rekordjog_start_sequence()
            wheel_messages_counter = 3
            while True:
                    ims = midi_inp.receive()
                    ims_2b = ims.bytes()[:2]

                    if ims_2b in JOG_CODES:
                        jog(ims)
    
                    elif ims_2b in TOUCH_ON_CODES:
                        deck_id = TOUCH_ON_CODES.index(ims_2b)
                        touch = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x7F])
                        midi_out.send(touch)

                    elif ims_2b in TOUCH_OFF_CODES:
                        deck_id = TOUCH_OFF_CODES.index(ims_2b)
                        release = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x00])
                        midi_out.send(release)
    
                    elif ims_2b in TEMPO_BIG_CODES:
                        deck_id = math.floor(TEMPO_BIG_CODES.index(ims_2b) / 2)
                        tempo_values[deck_id][0] = 127 - ims.bytes()[2]
                        tempo(deck_id)

                    elif ims_2b in TEMPO_SMALL_CODES:
                        deck_id = math.floor(TEMPO_SMALL_CODES.index(ims_2b) / 2)
                        tempo_values[deck_id][1] =  127 - ims.bytes()[2]
                        tempo(deck_id)
    except KeyboardInterrupt:
        print("\nClosing RekordJog, bye.")

if __name__ == "__main__":
    main()
