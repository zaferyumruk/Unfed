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

