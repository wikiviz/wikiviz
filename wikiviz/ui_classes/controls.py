class ControlsLayout(Widget):
    pass

class ResetSearchPopup(Popup):
    def __init__(self, on_reset_function, on_decline_function, **kwargs):
        super(ResetSearchPopup, self).__init__(**kwargs)
        self.on_reset_function = on_reset_function
        self.on_decline_function = on_decline_function
