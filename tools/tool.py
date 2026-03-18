class Tool:
    NAME = "tool"

    def __init__(self, app):
        self.app = app

    def on_press(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_release(self, event):
        pass

    def on_motion(self, event):
        pass

    def on_right_click(self, event):
        pass

    def on_key_press(self, event):
        pass

    def on_key_release(self, event):
        pass

    def cleanup(self):
        pass