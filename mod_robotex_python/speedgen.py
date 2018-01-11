from math import pi, cos

def torad(degree):
    return degree*pi/180

def cosines(ddir):
    out = [cos(torad(150 - ddir)), cos(torad(270-ddir)), cos(torad(30-ddir))]
    # right, back, left
    return out

def get_speeds(degrees, multiplier):
    fracts = cosines(degrees)
    fracts2 = map(lambda x: multiplier * x, fracts)
    fracts3 = map(int, map(round, fracts2))
    return fracts3[0], fracts3[1], fracts3[2]
    



