import pygame
import mido
from pprint import pprint

if __name__ == '__main__':
    outport = mido.open_output("IAC Driver Gamepad")
    pygame.init()
    done = False
    pygame.joystick.init()
    input_2_note = {}

    joystick_count = pygame.joystick.get_count()
    joysticks = []
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        input_2_note[joystick] = {}
        # Map MIDI to buttons
        note = 36
        for j in range(joystick.get_numbuttons()):
            input_2_note[joystick][f"b{j}"] = note
            note += 1

        for j in range(joystick.get_numhats()):
            for o, m in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:
                input_2_note[joystick][f"h{(o, m)}"] = note
                note += 1

        for j in range(joystick.get_numaxes()*2):
            input_2_note[joystick][f"a{j}"] = note
            input_2_note[joystick][f"a{-j}"] = note+1
            note += 2

        pprint(input_2_note[joystick])

    hat_state = (0, 0)
    while True:
        for joystick in joysticks:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    # print(f"Joystick button {event.button} pressed.")
                    print("note_on", input_2_note[joystick][f"b{event.button}"])
                    outport.send(mido.Message('note_on', channel=1,
                                              note=input_2_note[joystick][f"b{event.button}"], velocity=127))
                if event.type == pygame.JOYBUTTONUP:
                    # print(f"Joystick button {event.button} released.")
                    print("note_off", input_2_note[joystick][f"b{event.button}"])
                    outport.send(mido.Message('note_off', channel=1,
                                              note=input_2_note[joystick][f"b{event.button}"], velocity=0))
                # if event.type == pygame.JOYAXISMOTION:
                #     if event.value == 0:
                #         outport.send(mido.Message('note_off', channel=1,
                #                                   note=input_2_note[joystick][f"a{event.axis}"], velocity=0))
                #         outport.send(mido.Message('note_off', channel=1,
                #                                   note=input_2_note[joystick][f"a{-event.axis}"], velocity=0))
                #     elif event.value > 0:
                #         outport.send(mido.Message('note_on', channel=1,
                #                                   note=input_2_note[joystick][f"a{event.axis}"],
                #                                   velocity=int(event.value*127)))
                #         outport.send(mido.Message('note_off', channel=1,
                #                                   note=input_2_note[joystick][f"a{-event.axis}"], velocity=0))
                #     else:
                #         outport.send(mido.Message('note_on', channel=1,
                #                                   note=input_2_note[joystick][f"a{-event.axis}"],
                #                                   velocity=int(-event.value*127)))
                #         outport.send(mido.Message('note_off', channel=1,
                #                                   note=input_2_note[joystick][f"a{event.axis}"], velocity=0))

                if event.type == pygame.JOYAXISMOTION:
                    if event.value == 0:
                        outport.send(mido.Message('control_change', channel=1,
                                                  control=input_2_note[joystick][f"a{event.axis}"],
                                                  value=0))
                        outport.send(mido.Message('control_change', channel=1,
                                                  control=input_2_note[joystick][f"a{-event.axis}"],
                                                  value=0))
                    elif event.value > 0:
                        outport.send(mido.Message('control_change', channel=1,
                                                  control=input_2_note[joystick][f"a{event.axis}"],
                                                  value=int(event.value*127)))
                        # outport.send(mido.Message('control_change', channel=1,
                        #                           control=input_2_note[joystick][f"a{-event.axis}"],
                        #                           value=0))
                    else:
                        outport.send(mido.Message('control_change', channel=1,
                                                  control=input_2_note[joystick][f"a{-event.axis}"],
                                                  value=int(-event.value*127)))
                        # outport.send(mido.Message('control_change', channel=1,
                        #                           control=input_2_note[joystick][f"a{event.axis}"], value=0))

                if event.type == pygame.JOYHATMOTION:
                    pprint(event.value)
                    if hat_state != (0, 0):
                        outport.send(mido.Message('note_off', channel=2,
                                                  note=input_2_note[joystick][f"h{hat_state}"], velocity=0))
                    if event.value != (0, 0):
                        outport.send(mido.Message('note_on', channel=2,
                                                  note=input_2_note[joystick][f"h{event.value}"], velocity=127))
                    hat_state = event.value
