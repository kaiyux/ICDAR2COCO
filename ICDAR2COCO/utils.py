import math


def euc_distance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def azimuth_angle(x1, y1, x2, y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
        else:
            angle = math.pi / 2.0
    if y2 == y1:
        if x2 >= x1:
            angle = 0.0
        else:
            angle = math.pi
    elif x2 > x1:
        if y2 > y1:
            angle = math.pi / 2.0 - math.atan(dx / dy)
        else:
            angle = math.pi * 2 - math.atan(-dy / dx)
    elif x2 < x1:
        if y2 < y1:
            angle = 3 * math.pi / 2.0 - + math.atan(dx / dy)
        else:
            angle = math.pi - math.atan(dy / -dx)
    angle = angle * 180 / math.pi
    if angle > 180:
        return -(360 - angle)
    else:
        return angle


if __name__ == '__main__':
    print(azimuth_angle(0, 0, -0.1, 1))
    print(azimuth_angle(0, 0, 0, 1))
    print(azimuth_angle(0, 0, 0.1, 1))
    print(azimuth_angle(0, 0, 1, 1))
    print(azimuth_angle(0, 0, 1, 0.1))
    print(azimuth_angle(0, 0, 1, 0))
    print(azimuth_angle(0, 0, 1, -0.1))
    print(azimuth_angle(0, 0, 1, -1))
    print(azimuth_angle(0, 0, 0.1, -1))
    print(azimuth_angle(0, 0, 0, -1))
    print(azimuth_angle(0, 0, -0.1, -1))
    print(azimuth_angle(0, 0, -1, -1))
    print(azimuth_angle(0, 0, -1, -0.1))
    print(azimuth_angle(0, 0, -1, 0))
    print(azimuth_angle(0, 0, -1, 0.1))
    print(azimuth_angle(0, 0, -1, 1))
