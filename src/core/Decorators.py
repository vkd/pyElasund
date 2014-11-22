def checkStateDecorator(needState, error):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if self._state in needState:
                return func(self, *args, **kwargs)
            else:
                return error
        return wrapper
    return decorator


def returnOkIfNotError(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            result = 'ok'
        return result
    return wrapper


def changeStateOnSuccessful(stateCom):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result is None:
                self._changeState(stateCom)
            return result
        return wrapper
    return decorator
