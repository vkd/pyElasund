def checkStateDecorator(needState, error):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            print('deco')
            if self._state == needState:
                return func(self, *args, **kwargs)
            else:
                return error
        return wrapper
    return decorator
