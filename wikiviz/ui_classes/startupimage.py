from kivy.uix.image import Image
class StartupImage(Image):
    ''' The image that's shown on the startup screen
    '''
    def __init__(self, **kwargs):
        return super(StartupImage, self).__init__(**kwargs)
    def collide_point(self, x, y):
        return False
    def on_touch_down(self, touch):
        return
    def on_touch_up(self, touch):
        return
    def on_touch_move(self, touch):
        return
