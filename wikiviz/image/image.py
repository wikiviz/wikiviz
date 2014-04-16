from kivy.compat import queue
from os.path import join
from os import write, close, unlink, environ
from kivy.core.image import Image as CoreImage
from kivy.resources import resource_find
from kivy.properties import AliasProperty
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.scatter import Scatter
from kivy import kivy_data_dir
from kivy.clock import Clock
from kivy.cache import Cache
from kivy.core.image import ImageLoader, Image
from kivy.compat import PY2
from kivy.uix.widget import Widget as w
from collections import deque
from time import sleep
import threading
import mimetypes



from kivy.uix.button import Button as b
from kivy.uix.boxlayout import BoxLayout as bx
from kivy.uix.popup import Popup as p
from kivy.uix.scatter import ScatterPlane as sp, Scatter as s
from kivy.uix.pagelayout import PageLayout as pl
from kivy.uix.scrollview import ScrollView as sv
from kivy.uix.gridlayout import GridLayout as gl
from kivy.uix.textinput import TextInput as ti
from kivy.uix.label import Label as l



class ProxyImage(Image):
    '''Image returned by the Loader.image() function.

    :Properties:
        `loaded`: bool, defaults to False
            This value may be True if the image is already cached.

    :Events:
        `on_load`
            Fired when the image is loaded or changed.
    '''

    __events__ = ('on_load', )

    def __init__(self, arg, **kwargs):
        kwargs.setdefault('loaded', False)
        super(ProxyImage, self).__init__(arg, **kwargs)
        self.loaded = kwargs.get('loaded')

    def on_load(self):
        pass



class LoaderBase(object):
    '''Common base for the Loader and specific implementations.
    By default, the Loader will be the best available loader implementation.

    The _update() function is called every 1 / 25.s or each frame if we have
    less than 25 FPS.
    '''

    def __init__(self):
        self._loading_image = None
        self._error_image = None
        self._num_workers = 2
        self._max_upload_per_frame = 2
        self._paused = False
        self._resume_cond = threading.Condition()

        self._q_load = deque()
        self._q_done = deque()
        self._client = []
        self._running = False
        self._start_wanted = False
        self._trigger_update = Clock.create_trigger(self._update)

    def __del__(self):
        try:
            Clock.unschedule(self._update)
        except Exception:
            pass

    def _set_num_workers(self, num):
        if num < 2:
            raise Exception('Must have at least 2 workers')
        self._num_workers = num

    def _get_num_workers(self):
        return self._num_workers

    num_workers = property(_get_num_workers, _set_num_workers)
    '''Number of workers to use while loading (used only if the loader
    implementation supports it). This setting impacts the loader only on
    initialization. Once the loader is started, the setting has no impact::

        from kivy.loader import Loader
        Loader.num_workers = 4

    The default value is 2 for giving a smooth user experience. You could
    increase the number of workers, then all the images will be loaded faster,
    but the user will not been able to use the application while loading.
    Prior to 1.6.0, the default number was 20, and loading many full-hd images
    was completly blocking the application.

    .. versionadded:: 1.6.0
    '''

    def _set_max_upload_per_frame(self, num):
        if num is not None and num < 1:
            raise Exception('Must have at least 1 image processing per image')
        self._max_upload_per_frame = num

    def _get_max_upload_per_frame(self):
        return self._max_upload_per_frame

    max_upload_per_frame = property(_get_max_upload_per_frame,
                                    _set_max_upload_per_frame)
    '''The number of images to upload per frame. By default, we'll
    upload only 2 images to the GPU per frame. If you are uploading many
    small images, you can easily increase this parameter to 10 or more.
    If you are loading multiple full HD images, the upload time may have
    consequences and block the application. If you want a
    smooth experience, use the default.

    As a matter of fact, a Full-HD RGB image will take ~6MB in memory,
    so it may take time. If you have activated mipmap=True too, then the
    GPU must calculate the mipmap of these big images too, in real time.
    Then it may be best to reduce the :attr:`max_upload_per_frame` to 1
    or 2. If you want to get rid of that (or reduce it a lot), take a
    look at the DDS format.

    .. versionadded:: 1.6.0
    '''

    def _get_loading_image(self):
        if not self._loading_image:
            loading_png_fn = join(kivy_data_dir, 'images', 'image-loading.gif')
            self._loading_image = ImageLoader.load(filename=loading_png_fn)
        return self._loading_image

    def _set_loading_image(self, image):
        if isinstance(image, basestring):
            self._loading_image = ImageLoader.load(filename=image)
        else:
            self._loading_image = image

    loading_image = property(_get_loading_image, _set_loading_image)
    '''Image used for loading.
    You can change it by doing::

        Loader.loading_image = 'loading.png'

    .. versionchanged:: 1.6.0
        Not readonly anymore.
    '''

    def _get_error_image(self):
        if not self._error_image:
            error_png_fn = join(
                'atlas://data/images/defaulttheme/image-missing')
            self._error_image = ImageLoader.load(filename=error_png_fn)
        return self._error_image

    def _set_error_image(self, image):
        if isinstance(image, basestring):
            self._error_image = ImageLoader.load(filename=image)
        else:
            self._error_image = image

    error_image = property(_get_error_image, _set_error_image)
    '''Image used for error.
    You can change it by doing::

        Loader.error_image = 'error.png'

    .. versionchanged:: 1.6.0
        Not readonly anymore.
    '''

    def start(self):
        '''Start the loader thread/process.'''
        self._running = True

    def run(self, *largs):
        '''Main loop for the loader.'''
        pass

    def stop(self):
        '''Stop the loader thread/process.'''
        self._running = False

    def pause(self):
        '''Pause the loader, can be useful during interactions.

        .. versionadded:: 1.6.0
        '''
        self._paused = True

    def resume(self):
        '''Resume the loader, after a :meth:`pause`.

        .. versionadded:: 1.6.0
        '''
        self._paused = False
        self._resume_cond.acquire()
        self._resume_cond.notify_all()
        self._resume_cond.release()

    def _wait_for_resume(self):
        while self._running and self._paused:
            self._resume_cond.acquire()
            self._resume_cond.wait(0.25)
            self._resume_cond.release()

    def _load(self, kwargs):
        '''(internal) Loading function, called by the thread.
        Will call _load_local() if the file is local,
        or _load_urllib() if the file is on Internet.
        '''

        while len(self._q_done) >= (
                self.max_upload_per_frame * self._num_workers):
            sleep(0.1)

        self._wait_for_resume()

        filename = kwargs['filename']
        load_callback = kwargs['load_callback']
        post_callback = kwargs['post_callback']
        try:
            proto = filename.split(':', 1)[0]
        except:
            #if blank filename then return
            return
        if load_callback is not None:
            data = load_callback(filename)
        elif proto in ('http', 'https', 'ftp', 'smb'):
            data = self._load_urllib(filename, kwargs['kwargs'])
        else:
            data = self._load_local(filename, kwargs['kwargs'])

        if post_callback:
            data = post_callback(data)

        self._q_done.appendleft((filename, data))
        self._trigger_update()

    def _load_local(self, filename, kwargs):
        '''(internal) Loading a local file'''
        # With recent changes to CoreImage, we must keep data otherwise,
        # we might be unable to recreate the texture afterwise.
        return ImageLoader.load(filename, keep_data=True, **kwargs)

    def _load_urllib(self, filename, kwargs):
        '''(internal) Loading a network file. First download it, save it to a
        temporary file, and pass it to _load_local().'''
        if PY2:
            import urllib2 as urllib_request

            def gettype(info):
                return info.gettype()
        else:
            import urllib.request as urllib_request

            def gettype(info):
                return info.get_content_type()
        proto = filename.split(':', 1)[0]
        if proto == 'smb':
            try:
                # note: it's important to load SMBHandler every time
                # otherwise the data is occasionaly not loaded
                from smb.SMBHandler import SMBHandler
            except ImportError:
                Logger.warning(
                    'Loader: can not load PySMB: make sure it is installed')
                return
        import tempfile
        data = fd = _out_osfd = None

        print " ****in load url******\n*******************\n*******************"
        try:
            _out_filename = ''

            if proto == 'smb':
                # read from samba shares
                fd = urllib_request.build_opener(SMBHandler).open(filename)
            else:
                # read from internet
                fd = urllib_request.urlopen(filename)
            suffix = '.%s' % (filename.split('.')[-1])
            print suffix
            '''
            if '#.' in filename:
                # allow extension override from URL fragment
                suffix = '.' + filename.split('#.')[-1]
            else:
                ctype = gettype(fd.info())
                suffix = None
                if not suffix:
                    # strip query string and split on path
                    parts = filename.split('?')[0].split('/')[1:]
                    while len(parts) > 1 and not parts[0]:
                        # strip out blanks from '//'
                        parts = parts[1:]
                    if len(parts) > 1 and '.' in parts[-1]:
                        # we don't want '.com', '.net', etc. as the extension
                        suffix = '.' + parts[-1].split('.')[-1]
            '''
            _out_osfd, _out_filename = tempfile.mkstemp(
                prefix='kivyloader', suffix=suffix)
            idata = fd.read()
            fd.close()
            fd = None
            # write to local filename
            write(_out_osfd, idata)
            close(_out_osfd)
            _out_osfd = None
            # load data

            data = self._load_local(_out_filename, kwargs)

            # FIXME create a clean API for that
            for imdata in data._data:
                imdata.source = filename
        except Exception:
            Logger.exception('Loader: Failed to load image <%s>' % filename)
            # close file when remote file not found or download error
            try:
                close(_out_osfd)
            except OSError:
                pass
            return self.error_image
        finally:
            if fd:
                fd.close()
            if _out_osfd:
                close(_out_osfd)
            if _out_filename != '':
                unlink(_out_filename)

        return data

    def _update(self, *largs):
        '''(internal) Check if a data is loaded, and pass to the client.'''
        # want to start it ?
        if self._start_wanted:
            if not self._running:
                self.start()
            self._start_wanted = False

        # in pause mode, don't unqueue anything.
        if self._paused:
            self._trigger_update()
            return

        for x in range(self.max_upload_per_frame):
            try:
                filename, data = self._q_done.pop()
            except IndexError:
                return

            # create the image
            image = data  # ProxyImage(data)
            if not image.nocache:
                Cache.append('kv.loader', filename, image)

            # update client
            for c_filename, client in self._client[:]:
                if filename != c_filename:
                    continue
                # got one client to update
                client.image = image
                client.loaded = True
                client.dispatch('on_load')
                self._client.remove((c_filename, client))

        self._trigger_update()

    def image(self, filename, load_callback=None, post_callback=None,
              **kwargs):
        '''Load a image using the Loader. A ProxyImage is returned with a
        loading image. You can use it as follows::

            from kivy.app import App
            from kivy.uix.image import Image
            from kivy.loader import Loader

            class TestApp(App):
                def _image_loaded(self, proxyImage):
                    if proxyImage.image.texture:
                        self.image.texture = proxyImage.image.texture

                def build(self):
                    proxyImage = Loader.image("myPic.jpg")
                    proxyImage.bind(on_load=self._image_loaded)
                    self.image = Image()
                    return self.image

            TestApp().run()

        In order to cancel all background loading, call *Loader.stop()*.
        '''
        data = Cache.get('kv.loader', filename)
        if data not in (None, False):
            # found image, if data is not here, need to reload.
            return ProxyImage(data,
                              loading_image=self.loading_image,
                              loaded=True, **kwargs)

        client = ProxyImage(self.loading_image,
                            loading_image=self.loading_image, **kwargs)
        self._client.append((filename, client))

        if data is None:
            # if data is None, this is really the first time
            self._q_load.appendleft({
                'filename': filename,
                'load_callback': load_callback,
                'post_callback': post_callback,
                'kwargs': kwargs})
            if not kwargs.get('nocache', False):
                Cache.append('kv.loader', filename, False)
            self._start_wanted = True
            self._trigger_update()
        else:
            # already queued for loading
            pass

        return client

from threading import Thread
class _Worker(Thread):
    '''Thread executing tasks from a given tasks queue
    '''
    def __init__(self, pool, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.pool = pool
        self.start()

    def run(self):
        while self.pool.running:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()

class _ThreadPool(object):
    '''Pool of threads consuming tasks from a queue
    '''
    def __init__(self, num_threads):
        super(_ThreadPool, self).__init__()
        self.running = True
        self.tasks = queue.Queue()
        for _ in range(num_threads):
            _Worker(self, self.tasks)

    def add_task(self, func, *args, **kargs):
        '''Add a task to the queue
        '''
        self.tasks.put((func, args, kargs))

    def stop(self):
        self.running = False
        self.tasks.join()

class LoaderThreadPool(LoaderBase):
    def __init__(self):
        super(LoaderThreadPool, self).__init__()
        self.pool = None

    def start(self):
        super(LoaderThreadPool, self).start()
        self.pool = _ThreadPool(self._num_workers)
        Clock.schedule_interval(self.run, 0)

    def stop(self):
        super(LoaderThreadPool, self).stop()
        Clock.unschedule(self.run)
        self.pool.stop()

    def run(self, *largs):
        while self._running:
            try:
                parameters = self._q_load.pop()
            except:
                return
            self.pool.add_task(self._load, parameters)

Loader = LoaderThreadPool()

class Image(w):
    '''Image class, see module documentation for more information.
    '''

    source = StringProperty(None)
    '''Filename / source of your image.

    :attr:`source` is a :class:`~kivy.properties.StringProperty` and
    defaults to None.
    '''

    texture = ObjectProperty(None, allownone=True)
    '''Texture object of the image.

    Depending of the texture creation, the value will be a
    :class:`~kivy.graphics.texture.Texture` or a
    :class:`~kivy.graphics.texture.TextureRegion` object.

    :attr:`texture` is a :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    texture_size = ListProperty([0, 0])
    '''Texture size of the image.

    .. warning::

        The texture size is set after the texture property. So if you listen to
        the change on :attr:`texture`, the property texture_size will not be
        up-to-date. Use self.texture.size instead.
    '''

    def get_image_ratio(self):
        if self.texture:
            return self.texture.width / float(self.texture.height)
        return 1.

    mipmap = BooleanProperty(False)
    '''Indicate if you want OpenGL mipmapping to be applied to the texture.
    Read :ref:`mipmap` for more information.

    .. versionadded:: 1.0.7

    :attr:`mipmap` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''

    image_ratio = AliasProperty(get_image_ratio, None, bind=('texture', ))
    '''Ratio of the image (width / float(height).

    :attr:`image_ratio` is a :class:`~kivy.properties.AliasProperty` and is
    read-only.
    '''

    color = ListProperty([1, 1, 1, 1])
    '''Image color, in the format (r, g, b, a). This attribute can be used to
    'tint' an image. Be careful: if the source image is not gray/white, the
    color will not really work as expected.

    .. versionadded:: 1.0.6

    :attr:`color` is a :class:`~kivy.properties.ListProperty` and defaults to
    [1, 1, 1, 1].
    '''

    allow_stretch = BooleanProperty(False)
    '''If True, the normalized image size will be maximized to fit in the image
    box. Otherwise, if the box is too tall, the image will not be
    stretched more than 1:1 pixels.

    .. versionadded:: 1.0.7

    :attr:`allow_stretch` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    keep_ratio = BooleanProperty(True)
    '''If False along with allow_stretch being True, the normalized image
    size will be maximized to fit in the image box and ignores the aspect
    ratio of the image.
    Otherwise, if the box is too tall, the image will not be stretched more
    than 1:1 pixels.

    .. versionadded:: 1.0.8

    :attr:`keep_ratio` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True.
    '''

    keep_data = BooleanProperty(False)
    '''If True, the underlaying _coreimage will store the raw image data.
    This is useful when performing pixel based collision detection.

    .. versionadded:: 1.3.0

    :attr:`keep_data` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    anim_delay = NumericProperty(.25)
    '''Delay the animation if the image is sequenced (like an animated gif).
    If anim_delay is set to -1, the animation will be stopped.

    .. versionadded:: 1.0.8

    :attr:`anim_delay` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.25 (4 FPS).
    '''

    nocache = BooleanProperty(False)
    '''If this property is set True, the image will not be added to the
    internal cache. The cache will simply ignore any calls trying to
    append the core image.

    .. versionadded:: 1.6.0

    :attr:`nocache` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''

    def get_norm_image_size(self):
        if not self.texture:
            return self.size
        ratio = self.image_ratio
        w, h = self.size
        tw, th = self.texture.size

        # ensure that the width is always maximized to the containter width
        if self.allow_stretch:
            if not self.keep_ratio:
                return w, h
            iw = w
        else:
            iw = min(w, tw)
        # calculate the appropriate height
        ih = iw / ratio
        # if the height is too higher, take the height of the container
        # and calculate appropriate width. no need to test further. :)
        if ih > h:
            if self.allow_stretch:
                ih = h
            else:
                ih = min(h, th)
            iw = ih * ratio

        return iw, ih

    norm_image_size = AliasProperty(get_norm_image_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))
    '''Normalized image size within the widget box.

    This size will always fit the widget size and will preserve the image
    ratio.

    :attr:`norm_image_size` is a :class:`~kivy.properties.AliasProperty` and is
    read-only.
    '''

    def __init__(self, **kwargs):
        self._coreimage = None
        super(Image, self).__init__(**kwargs)
        self.bind(source=self.texture_update,
                  mipmap=self.texture_update)
        if self.source:
            self.texture_update()

    def texture_update(self, *largs):
        if not self.source:
            self.texture = None
        else:
            filename = resource_find(self.source)
            if filename is None:
                return Logger.error('Image: Error reading file {filename}'.
                                    format(filename=self.source))
            mipmap = self.mipmap
            if self._coreimage is not None:
                self._coreimage.unbind(on_texture=self._on_tex_change)
            try:
                self._coreimage = ci = CoreImage(filename, mipmap=mipmap,
                                                 anim_delay=self.anim_delay,
                                                 keep_data=self.keep_data,
                                                 nocache=self.nocache)
            except:
                self._coreimage = ci = None

            if ci:
                ci.bind(on_texture=self._on_tex_change)
                self.texture = ci.texture

    def on_anim_delay(self, instance, value):
        if self._coreimage is None:
            return
        self._coreimage.anim_delay = value
        if value < 0:
            self._coreimage.anim_reset(False)

    def on_texture(self, instance, value):
        if value is not None:
            self.texture_size = list(value.size)

    def _on_tex_change(self, *largs):
        # update texture from core image
        self.texture = self._coreimage.texture

    def reload(self):
        '''Reload image from disk. This facilitates re-loading of
        images from disk in case the image content changes.

        .. versionadded:: 1.3.0

        Usage::

            im = Image(source = '1.jpg')
            # -- do something --
            im.reload()
            # image will be re-loaded from disk

        '''
        self._coreimage.remove_from_cache()
        olsource = self.source
        self.source = ''
        self.source = olsource

    def on_nocache(self, *args):
        if self.nocache and self._coreimage:
            self._coreimage.remove_from_cache()
            self._coreimage._nocache = True


class AsyncImage(Image):
    '''Asynchronous Image class. See the module documentation for more
    information.

    .. note::

        The AsyncImage is a specialized form of the Image class. You may
        want to refer to the :mod:`~kivy.loader` documentation and in
        particular, the :class:`~kivy.loader.ProxyImage` for more detail
        on how to handle events around asynchronous image loading.
    '''

    def __init__(self, **kwargs):
        self._coreimage = None
        super(AsyncImage, self).__init__(**kwargs)
        self.bind(source=self._load_source)
        if self.source:
            self._load_source()

    def _load_source(self, *args):
        source = self.source
        if not source:
            if self._coreimage is not None:
                self._coreimage.unbind(on_texture=self._on_tex_change)
            self.texture = None
            self._coreimage = None
        else:
            if not self.is_uri(source):
                source = resource_find(source)
            self._coreimage = image = Loader.image(source,
                                                   nocache=self.nocache,
                                                   mipmap=self.mipmap)
            image.bind(on_load=self._on_source_load)
            image.bind(on_texture=self._on_tex_change)
            self.texture = image.texture

    def _on_source_load(self, value):
        image = self._coreimage.image
        if not image:
            return
        self.texture = image.texture

    def is_uri(self, filename):
        proto = filename.split('://', 1)[0]
        return proto in ('http', 'https', 'ftp', 'smb')

    def _on_tex_change(self, *largs):
        if self._coreimage:
            self.texture = self._coreimage.texture

    def texture_update(self, *largs):
        pass


class Node(Scatter):
    image = ObjectProperty(None)
    label = ObjectProperty(None)

    move = NumericProperty(0)
    flag = NumericProperty(0)

    def __init_(self, **kwargs):
        
        super(Node, self).__init__(kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.flag = 0
        self.register_event_type("on_click")

    def collide_point(self, x, y):
        x, y = self.to_local(x, y)
        return -1.1*self.width/8 <= x <= 1.2*self.width and -1.1*self.height/8 <= y <= 1.2*self.height

    def on_touch_up(self, touch):   
        if (self.collide_point(touch.x, touch.y) and self.move < 10):
            pagelayout = self.parent.parent
            uic = pagelayout.uic
            pagelayout.page = 2
            pagelayout.do_layout()
            pagelayout.summary.text = text1
            uic.blocked = True
            Animation(
                x=(-self.x)*uic.scale+window.Window.width/2,
                y=(-self.y)*uic.scale+window.Window.height/2,
                d=.5, t='in_quad').start(self.parent.parent.uic)
        if touch in self._touches:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
        return super(Node, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        self.move +=1
        return super(Node, self).on_touch_move(touch)


    def on_touch_down(self, touch):
        self.move = 0
        return super(Node, self).on_touch_down(touch)



    def display(self, link):
        self.image.source = link
        return

    def on_click(self):
        return


class Widget(w):
    pass
class Button(b):
    pass
class BoxLayout(bx):
    pass
class Popup(p):
    pass
class ScatterPlane(sp):
    pass
class Scatter(s):
    pass
class PageLayout(pl):
    pass
class ScrollView(sv):
    pass
class GridLayout(gl):
    pass
class TextInput(ti):
    pass
class Label(l):
    pass