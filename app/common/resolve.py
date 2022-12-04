import dill as pickle



def dump_object(value):
    """Dumps an object into a string for redis.  By default it serializes
    integers as regular string and pickle dumps everything else.
    """
    t = type(value)
    if t == int:
        return str(value).encode("ascii")
    return b"!" + pickle.dumps(value)

def load_object(value):
    """The reversal of :meth:`dump_object`.  This might be called with
    None.
    """
    if value is None:
        return None
    if value.startswith(b"!"):
        try:
            return pickle.loads(value[1:])
        except pickle.PickleError:
            return None
    try:
        return int(value)
    except ValueError:
        # before 0.8 we did not have serialization.  Still support that.
        return value
