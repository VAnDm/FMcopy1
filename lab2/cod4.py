import matplotlib.pyplot as plt
import numpy as np



def f(t):
    return a * np.e ** (-b * abs(t))
def furie(omega):
    x = np.e ** ((-1 * omega ** 2) / (4 * b))
    x = x * a / np.sqrt(2 * b)
    return x

a = 2
b = 1
print(furie(0))
fs1 = []
furs1 = []
t = -3
ts1 = [-3]
omega = -10
omegas1 = [-10]
fs1.append(f(t))
furs1.append(furie(omega))
while t < 3:
    t += 0.0001
    fs1.append(f(t))
    ts1.append(t)
while omega < 10:
    omega += 0.0003
    omegas1.append(omega)
    furs1.append(furie(omega))

leftpart = 0
rightpart = 0
t = -10000
omega = -10000
while t < 10000:
    t += 0.1
    leftpart = leftpart + abs((f(t))) ** 2 * 0.1
    omega = omega + 0.1
    rightpart = rightpart + abs(furie(omega)) ** 2 * 0.1
print(leftpart - rightpart)

a = 2
b = 1/2

fs2 = []
furs2 = []
t = -3
ts2 = [-3]
omega = -10
omegas2 = [-10]
fs2.append(f(t))
furs2.append(furie(omega))
while t < 3:
    t += 0.0001
    fs2.append(f(t))
    ts2.append(t)
while omega < 10:
    omega += 0.0003
    omegas2.append(omega)
    furs2.append(furie(omega))

leftpart = 0
rightpart = 0
t = -10000
omega = -10000
while t < 10000:
    t += 0.1
    leftpart = leftpart + abs(f(t)) ** 2 * 0.1
    omega = omega + 0.1
    rightpart = rightpart + abs(furie(omega)) ** 2 * 0.1
print(leftpart - rightpart)

a = 3
b = 1

fs3 = []
furs3 = []
t = -3
ts3 = [-3]
omega = -10
omegas3 = [-10]
fs3.append(f(t))
furs3.append(furie(omega))
while t < 3:
    t += 0.0001
    fs3.append(f(t))
    ts3.append(t)
while omega < 10:
    omega += 0.0003
    omegas3.append(omega)
    furs3.append(furie(omega))
plt.ion()
plt.plot(ts1, fs1, c = 'red', label = 'a = 2, b = 1')
plt.axis('equal')
plt.plot(ts2, fs2, c = 'blue', label = 'a = 2, b = 1/2')
plt.axis('equal')
plt.plot(ts3, fs3, c = 'green', label = 'a = 3, b = 1')
plt.axis('equal')
plt.draw()
plt.ioff()

plt.xlabel('t')
plt.ylabel('f(t)')
plt.legend()
plt.grid()
plt.show()

plt.ion()
plt.plot(omegas1, furs1, c = 'red', label = 'a = 2, b = 1')
#plt.axis('equal')
plt.plot(omegas2, furs2, c = 'blue', label = 'a = 2, b = 1/2')
#plt.axis('equal')
plt.plot(omegas3, furs3, c = 'green', label = 'a = 3, b = 1')
#plt.axis('equal')
plt.draw()
plt.ioff()

plt.xlabel('t')
plt.ylabel('^f(t)')
plt.legend()
plt.grid()
plt.show()

leftpart = 0
rightpart = 0
t = -10000
omega = -10000
while t < 10000:
    t += 0.1
    leftpart = leftpart + abs(f(t)) ** 2 * 0.1
    omega = omega + 0.1
    rightpart = rightpart + abs(furie(omega)) ** 2 * 0.1
print(leftpart - rightpart)