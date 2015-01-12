from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from ui_classes.searchbar import SearchButton
from kivy.properties import ListProperty
from kivy.clock import Clock
class ControlsLayout(BoxLayout):
    controls = ListProperty(None)
    def __init__(self, reset_function, **kwargs):
        super(ControlsLayout, self).__init__(**kwargs)
        self.search_reset = reset_function
        self.register_event_type("on_initialize")
        Clock.schedule_once(self.on_initialize)

    def on_initialize(self, *args):
        temp = SearchButton(self.add_reset_popup)
        self.controls.append(temp)
        self.add_widget(temp)

    def add_reset_popup(self):
        self.search_reset()
    def on_touch_down(self, touch):
        '''
        Determine action on touch based on current state
        '''
        # do nothing if touch causes children to exceed screen bounds (?)
        x, y = touch.x, touch.y
        # otherwise respond to touch
        return super(ControlsLayout, self).on_touch_down(touch)
    def on_touch_move(self, touch):
        '''
        Determine action on touch based on current state
        '''
        # do nothing if touch causes children to exceed screen bounds (?)
        x, y = touch.x, touch.y
        # otherwise respond to touch
        return super(ControlsLayout, self).on_touch_move(touch)
    def on_touch_up(self, touch):
        '''
        Determine action on touch based on current state
        '''
        # do nothing if touch causes children to exceed screen bounds (?)
        x, y = touch.x, touch.y
        # otherwise respond to touch
        super(ControlsLayout, self).on_touch_up(touch)
        if self.collide_point(x,y):
            self.search_reset()
            return True
        return False

class ResetSearchPopup(Popup):
    def __init__(self, on_reset_function, on_decline_function, **kwargs):
        super(ResetSearchPopup, self).__init__(**kwargs)
        self.on_reset_function = on_reset_function
        self.on_decline_function = on_decline_function
    def on_touch_down(self, touch):
        return True
    def on_touch_move(self,touch):
        return True
    def on_touch_up(self,touch):
        for eachChild in self.children:
            if eachChild.collide_point(touch.x,touch.y):
                eachChild.on_touch_up(touch)
                return True
        return True



