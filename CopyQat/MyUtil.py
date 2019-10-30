import threading

def synchronized_method(method):

    outer_lock = threading.Lock()
    lock_name = "__"+method.__name__+"_lock"+"__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method

def center_window(self, width=0, height=0):
    screen_width = self.parent.winfo_screenwidth()
    screen_height = self.parent.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))
