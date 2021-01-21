# implementation of polar/rect functions using non-cmath

try:
    import cmath
    no_cmath = False
except:
    no_cmath = True
    import math

if no_cmath:
    def _to_polar_angle(x, y):
        """
        Converts an x,y to angle.
        :param x: x coordinate
        :param y: y coordinate
        :returns: angle in radians
        """
        return math.atan2(y, x)


    def _to_polar_radius(x, y):
        """
        Converts an x,y to radius.
        :param x: x coordinate
        :param y: y coordinate
        :returns: radius
        """
        return math.sqrt( (x*x) + (y*y) )


    def _to_rect_x(r, a):
        """
        Converts an r, a to x coordinate
        :param r: radius
        :param a: angle
        :returns: x coordinate
        """
        return r * math.cos(a)


    def _to_rect_y(r, a):
        """
        Converts an r, a to y coodinate
        :param r: radius
        :param a: angle
        :returns: y coordinate
        """
        return r * math.sin(a)


def polar(x, y):
    """
    Converts an x, y to polar coordinates
    :param x: x coordinate
    :param y: y coordinate
    :returns: (radius, angle)
    """
    if no_cmath:
        return _to_polar_radius(x, y), _to_polar_angle(x, y)
    return cmath.polar(complex(x, y))

def rect(r, a):
    """
    Converts an r, a to regular coordinates
    :param r: radius
    :param a: angle
    :returns: (x, y)
    """
    if no_cmath:
        return _to_rect_x(r, a), _to_rect_y(r, a)
    coords = cmath.rect(r, a)
    return coords.real, coords.imag

