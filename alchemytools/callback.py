

class Callback:
    def __init__(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError("Argument func must be a callable!")

        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        try:
            self.func(*self.args, **self.kwargs)
        except:
            # FIXME: silently failing
            pass
