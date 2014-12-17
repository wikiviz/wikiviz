from kivy.uix.scrollview import ScrollView
    
class UISummary(ScrollView):
    flag = BooleanProperty(False)
    text = StringProperty(None)

    label = ObjectProperty(None)
    image = ObjectProperty(None)

    def on_touch_up(self, touch):
        if self.flag:
            self.flag = False
            self.parent.page -=1
        return super(UISummary, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return
        if self._touch is not touch:
            # touch is in parent
            touch.push()
            touch.apply_transform_2d(self.to_local)
            super(ScrollView, self).on_touch_move(touch)
            touch.pop()
            return self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True

        uid = self._get_uid()
        ud = touch.ud[uid]
        mode = ud['mode']

        # check if the minimum distance has been travelled
        if mode == 'unknown' or mode == 'scroll':
            if self.do_scroll_x and self.effect_x:
                width = self.width
                if self.scroll_type != ['bars']:
                    self.effect_x.update(touch.x)
            if self.do_scroll_y and self.effect_y:
                height = self.height
                if self.scroll_type != ['bars']:
                    self.effect_y.update(touch.y)

        if (touch.dy !=0 and abs(touch.dx/touch.dy) >1) or (touch.dy==0 and abs(touch.dx) > 3):
            self.flag = True
            return True

        if mode == 'unknown':
            ud['dx'] += abs(touch.dx)
            ud['dy'] += abs(touch.dy)
            if ud['dx'] > self.scroll_distance:
                if not self.do_scroll_x:
                    # touch is in parent, but _change expects window coords
                    touch.push()
                    touch.apply_transform_2d(self.to_local)
                    touch.apply_transform_2d(self.to_window)
                    self._change_touch_mode()
                    touch.pop()
                    return
                mode = 'scroll'

            if ud['dy'] > self.scroll_distance:
                if not self.do_scroll_y:
                    # touch is in parent, but _change expects window coords
                    touch.push()
                    touch.apply_transform_2d(self.to_local)
                    touch.apply_transform_2d(self.to_window)
                    self._change_touch_mode()
                    touch.pop()
                    return
                mode = 'scroll'
            ud['mode'] = mode

        if mode == 'scroll':
            ud['dt'] = touch.time_update - ud['time']
            ud['time'] = touch.time_update
            ud['user_stopped'] = True

        return True
