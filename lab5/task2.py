import numpy as np
import matplotlib.pyplot as plt
import os

a1 = 1
omega1 = 5 * np.pi
phi1 = 11 * np.pi
a2 = 2
omega2 = 3 * np.pi
phi2 = 13 * np.pi
b = 7

#def y1(t):
    #x = a1 * np.sin(omega1 * t + phi1) + a2 * np.sin(omega2 * t + phi2)
    #return x
def y1(t):
    x = np.sinc(b * t)
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
dt = 0.1
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

Tmaliy = 1.5
tdiscmaliy = []
y1discmaliy = []
for i in range(len(tdisc)):
    if tdisc[i] >= -Tmaliy and tdisc[i] <= Tmaliy:
        tdiscmaliy.append(tdisc[i])
        y1discmaliy.append(y1disc[i])
y1intergraph = []
for i in range(len(t)):
    a = yinterpol(t[i], tdiscmaliy, y1discmaliy, dt)
    y1intergraph.append(a)

plt.ion()
plt.plot(t, y1nepr, c = 'red', linewidth = 6, label = 'y1(t)')
plt.plot(tdiscmaliy, y1discmaliy, linewidth = 3, c = 'green', label = 'y1_disc(t)')
plt.plot(t, y1intergraph, c = 'black', linestyle = '--', label = 'y1_inter(t)')
plt.draw()
plt.xlim([-3, 3])
plt.ioff()

plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()

V = 1/(2 * 0.01)
dv = 1/(2 * T)
vnepr = []
c = -V
while c < V:
    vnepr.append(c)
    c += dv

Vdisc = 1/(2 * dt)
dvdisc = 1/(2 * Tmaliy)
#vdisc = []
#c = -Vdisc
#while c < Vdisc:
    #vdisc.append(c)
    #c += dvdisc
vdisc = np.arange(-Vdisc, Vdisc, dvdisc)

furnepr = np.abs(np.fft.fftshift(np.fft.fft(y1nepr)) * 0.01)
furdisc = np.abs(np.fft.fftshift(np.fft.fft(y1discmaliy)) * dt)
furinter = np.abs(np.fft.fftshift(np.fft.fft(y1intergraph)) * 0.01)

plt.ion()
plt.plot(vnepr, furnepr, c = 'red', linewidth = 6, label = 'Модуль Фурье-образа y1(t)')
plt.plot(vdisc, furdisc, linewidth = 3, c = 'green', label = 'Модуль Фурье-образа y1_disc(t)')
plt.plot(vnepr, furinter, c = 'black', linestyle = '--', label = 'Модуль Фурье-образа y1_inter(t)')
plt.axvline(x = 3.5, c = 'blue', linestyle = '--', label = 'v = B')
plt.axvline(x = -3.5, c = 'blue', linestyle = '--', label = 'v = -B')
plt.draw()
plt.xlim([-5, 5])
plt.ioff()

plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()
