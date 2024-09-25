import mido

def jog_incremental(ims, midi_out, wheel_messages_counter, TURN_CLOCK_SPEED, TURN_COUNTER_SPEED, JOG_SIDE_CODE, JOG_TOP_CODE):
    if ims.control == JOG_SIDE_CODE or ims.control == JOG_TOP_CODE:
        wheel_messages_counter += 1
        if wheel_messages_counter % 4 == 0:
            if ims.value == 0x01:
                midi_out.send(mido.Message('control_change', channel=ims.channel, control=ims.control, value=TURN_CLOCK_SPEED))
            elif ims.value == 0x7F:
                midi_out.send(mido.Message('control_change', channel=ims.channel, control=ims.control, value=TURN_COUNTER_SPEED))
    return wheel_messages_counter
