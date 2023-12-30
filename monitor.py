import mido


rtmidi = mido.Backend('mido.backends.rtmidi', load=True)
inp = rtmidi.open_input("Allen&Heath Xone:4D XONE:4D")
# out = rtmidi.open_output("PIONEER DDJ-SX", True)



while True:
    msg = inp.receive().bytes()
    msg_b = list(map(hex, msg))
    if msg_b != ['0xf8']:
        print(msg_b)




