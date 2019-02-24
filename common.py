import numpy as np

def checkInRange(r, center, pos):
    xdiff = center[0] - pos[0]
    if abs(xdiff) > r:
        return False
    ydiff = center[1] - pos[1]
    if abs(ydiff) > r:
        return False
    if xdiff + ydiff < r:
        return True
    if xdiff**2 + ydiff**2 < r**2:
        return True


def checkStrConvert(s, checktype):
    try:
        if type(s) is str:
            checktype(s)
            return True
        else:
            return False
    except ValueError:
        return False

# ! check this
def unitvec(alist):
    norm = np.linalg.norm(alist)
    if norm == 0.0:
        return [0.0] * len(alist)
    return [val / norm for val in alist]


def maxnorm(alist):
    max_entry = sum(alist)
    return [val / max_entry for val in alist]


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unitvec(v1)
    v2_u = unitvec(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * 180 / np.pi

def angle_vector(v):
    return np.arctan2(v[1], v[0]) * 180 / np.pi
