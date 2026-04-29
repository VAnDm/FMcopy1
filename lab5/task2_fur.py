import numpy as np
import matplotlib.pyplot as plt
import os

a1 = 1
omega1 = 5 * np.pi
phi1 = 11 * np.pi
a2 = 2
omega2 = 3 * np.pi
phi2 = 13 * np.pi

def y1(t):
    x = a1 * np.sin(omega1 * t + phi1) + a2 * np.sin(omega2 * t + phi2)
    return x

def yinterpol(t, tdiscmaliy, ydiscmaliy, dt):
    x = 0
    for i in range(len(tdiscmaliy)):
        x = x + ydiscmaliy[i] * np.sinc((t - tdiscmaliy[i]) / dt)
    return x


T = 100
t = []
c = -T
while c < T:
    t.append(c)
    c += 0.01
dt = 0.19
c = -T
tdisc = []
while c < T:
    tdisc.append(c)
    c += dt
y1nepr = []
for i in t:
    y1nepr.append(y1(i))
y1disc = []
for i in tdisc:
    y1disc.append(y1(i))

Tmaliy = 10
tdiscmaliy = []
y1discmaliy = []
for i in range(len(tdisc)):
    if tdisc[i] >= -Tmaliy and tdisc[i] <= Tmaliy:
        tdiscmaliy.append(tdisc[i])
        y1discmaliy.append(y1disc[i])
yintergraph = []
for i in range(len(t)):
    a = yinterpol(t[i], tdiscmaliy, y1discmaliy, dt)
    yintergraph.append(a)

