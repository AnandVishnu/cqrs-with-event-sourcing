from functools import singledispatch, update_wrapper
# based on single dispatch
# https://docs.python.org/3/library/functools.html#functools.singledispatch
def overloading(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper
