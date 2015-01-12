from kivy.uix.popup import Popup
from kivy.properties import StringProperty 

class UISummary(Popup):
    text = StringProperty(None)

    def __init__(self, title, text, on_done, **kwargs):
        super(UISummary, self).__init__(**kwargs)
        self.title = title
        self.text = text
        self.on_done = on_done
    def on_touch_down(self, touch):
        return True
    def on_touch_move(self,touch):
        return True
    def on_touch_up(self,touch):
        for eachChild in self.children:
            if eachChild.collide_point(touch.x,touch.y):
                self.on_done()
                return True
        return True

