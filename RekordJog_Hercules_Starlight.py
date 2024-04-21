import math
import mido

rtmidi = mido.Backend('mido.backends.rtmidi', load=True)
midi_inp = rtmidi.open_input("DjControl Starlight")
midi_out = rtmidi.open_output("PIONEER DDJ-SX", True)

# The JOG_MULTIPLIER is required for smooth jog operation. 
# Pioneer controllers seem to be sending MIDI signal at a much higher rate than XONE:4D. 
# If you send one fake Pioneer message for each Xone jog message, scratching sounds unnatural.
# You need to test different values for other controllers.
JOG_MULTIPLIER = 1

CONV_J_VAL = {
    1:65,   #0
    1:66,   #1
    1:67,   #1
    1:69,   #2
    1:71,  #2
    1:73,  #2
    1:75,  #2
    1:83,  #5
    
    127:63,
    127:62,
    127:61,
    127:59,
    127:57,
    127:55,
    127:53,
    127:45
    }

PITCH_BEND_CODES = [
    [0XB1, 0X09],
    [0XB2, 0X09],
]

JOG_CODES = [
    [0xB1, 0x0A],
    [0xB2, 0x0A],
]

JOG_SHIFTED_CODES = [
    180, 181
]

TOUCH_ON_CODES = [
    [0x91, 0x08,0x7f],
    [0x92, 0x08,0x7f],
]

TOUCH_OFF_CODES = [
    [0x91, 0x08,0x00],
    [0x92, 0x08,0x00],
]

PITCHBEND_CODES = [
    [0xb1, 0x09],
    [0xb2, 0x09],
]

TEMPO_CODES = [
    [0xb1, 0x08],
    [0xb2, 0x08],
]

tempo_values = [
    [63, 63],
    [63, 63],
]

def jog(msg):
    id = JOG_CODES.index(msg.bytes()[:2])
    v = CONV_J_VAL[msg.bytes()[2]]
    ms = mido.Message.from_bytes([176+id, 0x22, v])
    
    for i in range(JOG_MULTIPLIER):
        midi_out.send(ms)

def pitchBend(msg):
    id = PITCHBEND_CODES.index(msg.bytes()[:2])
    v = CONV_J_VAL[msg.bytes()[2]]
    print(v)
    ms = mido.Message.from_bytes([176+id, 0x23, v])
    
    for i in range(JOG_MULTIPLIER):
        midi_out.send(ms)
        v = int(v/1) #random sensitivity value

def search(msg):
    id = JOG_SHIFTED_CODES.index(msg.bytes()[:2][0])
    v = CONV_J_VAL[msg.bytes()[2]]
    ms = mido.Message.from_bytes([176+id, 0x1F, v])
    midi_out.send(ms)
    
def tempo(id):
    msb = mido.Message.from_bytes([0xB0+id, 0x00, tempo_values[id][0]])
    lsb = mido.Message.from_bytes([0xB0+id, 0x20, tempo_values[id][1]])
    midi_out.send(msb)
    midi_out.send(lsb)

while True:
    ims = midi_inp.receive()
    ims_1b = ims.bytes()[:1][0]
    ims_2b = ims.bytes()[:2]
    ims_3b = ims.bytes()[:3]
    
    if ims_2b in JOG_CODES:
        jog(ims)
    
    elif ims_2b in PITCHBEND_CODES:
        pitchBend(ims)
    
    elif ims_1b in JOG_SHIFTED_CODES:
        search(ims)
    
    elif ims_3b in TOUCH_ON_CODES:
        deck_id = TOUCH_ON_CODES.index(ims_3b)
        touch = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x7F])
        midi_out.send(touch)

    elif ims_3b in TOUCH_OFF_CODES:
        deck_id = TOUCH_OFF_CODES.index(ims_3b)
        release = mido.Message.from_bytes([0x90+deck_id, 0x36, 0x00])
        midi_out.send(release)
    
    elif ims_2b in TEMPO_CODES:
        deck_id = math.floor(TEMPO_CODES.index(ims_2b))
        tempo_values[deck_id][0] = 127 - ims.bytes()[2]
        tempo(deck_id)