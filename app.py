import math
import mido


mido.Backend('mido.backends.rtmidi', load=True)
midi_inp = mido.open_input("controller")
midi_out = mido.open_output("PIONEER DDJ-SX", True)

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


JOG_CODES = {
    (0xBF, 0x25):0,
    (0xBF, 0x2D):1,
    (0xBE, 0x25):2,
    (0xBE, 0x2D):3,
}


TOUCH_ON_CODES = {
    (0x9F, 0x26):0,
    (0x9F, 0x46):1,    
    (0x9E, 0x26):2,
    (0x9E, 0x46):3,
}


TOUCH_OFF_CODES = {
    (0x8F, 0x26):0,
    (0x8F, 0x46):1,    
    (0x8E, 0x26):2,
    (0x8E, 0x46):3,
}


TEMPO_BIG_CODES = {
    (0xbf, 0x11):0,
    (0xbe, 0x11):1,
    (0xbf, 0x1f):2,
    (0xbe, 0x1f):3,
    (0xbf, 0x13):4,
    (0xbe, 0x13):5,
    (0xbf, 0x1d):6,
    (0xbe, 0x1d):7,
}


TEMPO_SMALL_CODES = {
    (0xbf, 0x10):0,
    (0xbe, 0x10):1,
    (0xbf, 0x1e):2,
    (0xbe, 0x1e):3,
    (0xbf, 0x12):4,
    (0xbe, 0x12):5,
    (0xbf, 0x1c):6,
    (0xbe, 0x1c):7,
}


def jog(msg):
    id = JOG_CODES[tuple(msg.bytes()[:2])]
    v = CONV_J_VAL[tuple(msg.bytes()[2])]

    ms = mido.Message.from_bytes([176+id, 0x22, v])

    for i in range(JOG_MULTIPLIER):
        midi_out.send(ms)

def tempo(id):
    msb = mido.Message.from_bytes([0xB0+id, 0x00, tempo_values[id][0]])
    lsb = mido.Message.from_bytes([0xB0+id, 0x20, tempo_values[id][1]])
    midi_out.send(msb)
    midi_out.send(lsb)

while True:
    ims = midi_inp.receive()
    ims_2b = tuple(ims.bytes()[:2])

    if ims_2b in JOG_CODES:
        jog(ims)
    
    elif ims_2b in TOUCH_ON_CODES:
        deck_id = TOUCH_ON_CODES[ims_2b]
        touch = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x7F])
        midi_out.send(touch)

    elif ims_2b in TOUCH_OFF_CODES:
        deck_id = TOUCH_OFF_CODES[ims_2b]
        release = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x00])
        midi_out.send(release)
    
    elif ims_2b in TEMPO_BIG_CODES:
        deck_id = math.floor(TEMPO_BIG_CODES[ims_2b] / 2)
        tempo_values[deck_id][0] = 127 - ims.bytes()[2]
        tempo(deck_id)

    elif ims_2b in TEMPO_SMALL_CODES:
        deck_id = math.floor(TEMPO_SMALL_CODES[ims_2b] / 2)
        tempo_values[deck_id][1] =  127 - ims.bytes()[2]
        tempo(deck_id)

