import math

def I_L( lx, ly, t):
    print( ((lx - t) * t * t/2 + ly * t * ly/2)/(lx*t + (ly - t)*t))
class L:
    def __init__(self,  lx, ly, t) -> None:
        self.Cx = ((lx - t) * t * t/2 + ly * t * ly/2)/(lx*t + (ly - t)*t)
        self.Cy = ((ly - t) * t * t/2 + lx * t * lx/2)/(ly*t + (lx - t)*t)
        self.m = (lx*t + (ly - t)*t)
def Ix(l1, l2, l3, t1, t2, t3):
    return l1*t1**3/12 + l2**3*t2/12 * 2 + ( l3*t3**3/12 + l3*t3*(t1/2 + t2/2)**2 ) * 2 + ( (l3 - t3)**3 *t3/12 + (l3-t3)*t3*(t1/2 + l3/2)**2 ) * 2
def Iy(l1, l2, l3, t1, t2, t3):
    return l2*t2**3/12 + l2*t2 * (l1/2 + t2)**2  +( t3*l3**3/12 + t3*l3 * (t1/2-t3)**2 ) * 2 + (l3-t3)**3 * t3/12 + l3


class Beam:
    def __init__(self,  l, t) -> None:
        self.Cx = 0.0
        self.Cy = 0.0
        self.m = (l*t)


print(Ix(0.1484, 0.04, 0.02, 0.0008, 0.0008, 0.0015))
#1.617510131666667e-08