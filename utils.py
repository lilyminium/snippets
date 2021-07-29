from typing import Any, Iterable

def cached(func):
    """Cache a property within a class.
    Requires the Class to have a cache dict called ``_cache``.
    Example
    -------
    How to add a cache for a variable to a class by using the `@cached`
    decorator::
       class A(object):
           def__init__(self):
               self._cache = dict()
           @cached('keyname')
           def size(self):
               # This code gets run only if the lookup of keyname fails
               # After this code has been ran once, the result is stored in
               # _cache with the key: 'keyname'
               return size
    .. note::
        Adapted from MDAnalysis. This code is GPL licensed.
    """

    key = func.__name__

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return self._cache[key]
        except KeyError:
            self._cache[key] = ret = func(self, *args, **kwargs)
            return ret
    return property(wrapper)



def is_iterable(obj: Any) -> bool:
    """Returns ``True`` if `obj` can be iterated over and is *not* a string
    nor a :class:`NamedStream`

    .. note::
        
        This is adapted from MDAnalysis.lib.util.iterable.
        It is GPL licensed.
    """
    if isinstance(obj, str):
        return False
    if hasattr(obj, "__next__") or hasattr(obj, "__iter__"):
        return True
    try:
        len(obj)
    except (TypeError, AttributeError):
        return False
    return True


def as_iterable(obj: Any) -> Iterable:
    """Returns `obj` so that it can be iterated over.

    A string is *not* considered an iterable and is wrapped into a
    :class:`list` with a single element.

    .. note::

        This is barely a function but I guess it's MIT.

    See Also
    --------
    is_iterable
    """
    if not is_iterable(obj):
        obj = [obj]
    return obj
