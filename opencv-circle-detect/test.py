from math import cos, pi, ceil
def torad(degs):
    return degs*pi / 180


def motor_vels(des_angle):
    return [cos(torad(des_angle - 120))/5, cos(torad(des_angle-240))/5, cos(torad(des_angle))/5]

def vels_to_3dec(vel_triplet):
    returnlist = []
    for vel in vel_triplet:
        vel = ceil(vel*1000)/1000
        returnlist.append(vel)
    return returnlist

#triangle angles
print vels_to_3dec(motor_vels(180))
print vels_to_3dec(motor_vels(60))
print vels_to_3dec(motor_vels(300))

#square angles
print vels_to_3dec(motor_vels(180))
print vels_to_3dec(motor_vels(90))
print vels_to_3dec(motor_vels(0))
print vels_to_3dec(motor_vels(270))

#circle
for i in range(1,36):
    print vels_to_3dec(motor_vels(i*10))


