from math import pi, cos

def torad(degree):
    return degree*pi/180

def cosines(ddir):
    out = [cos(torad(270 - ddir)), cos(torad(30-ddir)), cos(torad(150-ddir))]
    return out

def sendcmd(degrees):
    fracts = cosines(degrees)
    fracts2 = map(lambda x: 255 * x, fracts)
    fracts3 = map(int, map(round, fracts2))
    
    out = ""
    for num in fracts3:
        out += str(num)
        out += ","
    out += "\n"

    return out

print sendcmd(0)



