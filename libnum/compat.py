try:
    basestring = basestring
    xrange = xrange
except NameError:
    basestring = str
    xrange = range
