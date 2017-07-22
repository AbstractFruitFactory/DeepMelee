import pad

class Fox:
    def __init__(self):
        self.action_list = []
        self.last_action = 0

    def advance(self, state, this_pad):
        while self.action_list:
            wait, func, args = self.action_list[0]
            if state.frame - self.last_action < wait:
                return
            else:
                self.action_list.pop(0)
                if func is not None:
                    func(*args)
                self.last_action = state.frame
        else:
            # Eventually this will point at some decision-making thing.
            self.shinespam(this_pad)

    def shinespam(self, this_pad):
        self.action_list.append((0, this_pad.tilt_stick, [pad.Stick.MAIN, 0.5, 0.0]))
        self.action_list.append((0, this_pad.press_button, [pad.Button.B]))
        self.action_list.append((1, this_pad.release_button, [pad.Button.B]))
        self.action_list.append((0, this_pad.tilt_stick, [pad.Stick.MAIN, 0.5, 0.5]))
        self.action_list.append((0, this_pad.press_button, [pad.Button.X]))
        self.action_list.append((1, this_pad.release_button, [pad.Button.X]))
        self.action_list.append((1, None, []))
