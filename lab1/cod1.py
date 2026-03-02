import matplotlib.pyplot as plt
import numpy as np
from math import e
from math import sin
from math import cos
from math import sqrt

def Ref(t):
    ans = 0
    a = (t + 1) % 8 - 1
    if a < 1:
        ans = 2
    elif a < 3:
        ans = 4 - 2 * a
    elif a < 5:
        ans = -2
    else:
        ans = -12 + 2 * a
    return ans

def Imf(t):
    ans = 0
    a = (t + 1) % 8 - 1
    if a < 1:
        ans = 2 * a
    elif a < 3:
        ans = 2
    elif a < 5:
        ans = 8 - 2 * a
    else:
        ans = -2
    return ans


t = 0
res = []
ims = []
while t < 8:
    res.append(Ref(t))
    ims.append(Imf(t))
    t += 0.0001

plt.ion()
plt.plot(res, ims, c = 'blue')
plt.axis('equal')
plt.draw()
plt.ioff()

plt.xlabel("Re(f(t))")
plt.ylabel("Im(f(t))")
plt.legend()
plt.grid()
plt.show()
