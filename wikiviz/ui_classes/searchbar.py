from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

class SearchBar(Widget):
    def __init__(self, on_search_function, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.on_search_function = on_search_function
    def on_touch_down(self, touch):
        return super(SearchBar, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        return super(SearchBar, self).on_touch_up(touch)

class MyTextInput(TextInput):
    ''' Custom TextInput class
    '''
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.register_event_type("on_enter")

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        ''' Override keyboard events to allow for easy editing of text
        '''
        _is_osx = False
        # Keycodes on OSX:
        ctrl, cmd = 64, 1024
        key, key_str = keycode

        # This allows *either* ctrl *or* cmd, but not both.
        is_shortcut = (modifiers == ['ctrl'] or (
            _is_osx and modifiers == ['meta']))
        is_interesting_key = key in (list(self.interesting_keys.keys()) + [27])

        if not self._editable:
            # duplicated but faster testing for non-editable keys
            if text and not is_interesting_key:
                if is_shortcut and key == ord('c'):
                    self._copy(self.selection_text)
            elif key == 27:
                self.focus = False
            return True

        if text and not is_interesting_key:
            self._hide_handles(self._win)
            self._hide_cut_copy_paste()
            self._win.remove_widget(self._handle_middle)
            if is_shortcut:
                if key == ord('x'):  # cut selection
                    self._cut(self.selection_text)
                elif key == ord('c'):  # copy selection
                    self._copy(self.selection_text)
                elif key == ord('v'):  # paste selection
                    self._paste()
                elif key == ord('a'):  # select all
                    self.select_all()
                elif key == ord('z'):  # undo
                    self.do_undo()
                elif key == ord('r'):  # redo
                    self.do_redo()
            else:
                if self._selection:
                    self.delete_selection()
                self.insert_text(text)
            return

        if key == 27:  # escape
            self.focus = False
            return True
        elif key == 9:  # tab
            self.insert_text(u'\t')
            return True
        elif key == 13: # enter
            self.dispatch("on_enter")
            return True

        k = self.interesting_keys.get(key)
        if k:
            key = (None, None, k, 1)
            self._key_down(key)


    def on_enter(self):
        #see kivy file for implementation
        return

class SearchButton(Image):
    pass
