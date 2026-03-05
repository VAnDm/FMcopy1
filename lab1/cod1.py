import matplotlib.pyplot as plt
import numpy as np

i = 1j

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


def cn(n):
    if n == 0:
        return 0 + 0 * i
    else:
        k1 = 1/((np.pi ** 2) * (n ** 2))
        e1 = np.exp(-(7/4) * i * np.pi * n)
        e2 = np.exp((1/2) * i * np.pi * n)
        e3 = np.exp(i * np.pi * n)
        e4 = np.exp((3/2) * i * np.pi * n)
        e5 = np.exp(2 * i * np.pi * n)
        c = k1 * (1 + i) * e1 * (2 - 2 * i - 4 * e2 + 4 * i * e3 + 4 * e4 + n * np.pi - e5 * (2 + n * np.pi + 2 * i))
        return c

N = 3
k = -1 * N
ns = []
cns = []
for p in range(2 * N + 1):
    ns.append(k)
    cns.append(cn(k))
    k = k + 1
#print(*cns)

t = 0
ts = []
res = []
ims = []
resg = []
imsg = []
while t < 16:
    ts.append(t)
    res.append(Ref(t))
    ims.append(Imf(t))
    ch = 0 + 0 * i
    for j in range(2 * N + 1):
        n = ns[j]
        c = cns[j]
        ch = ch + c * np.exp(i * (2 * np.pi * n / 8) * t)
    re = ch.real
    resg.append(re)
    im = ch.imag
    imsg.append(im)
    t += 0.0001

plt.ion()
plt.plot(ts, ims, c = 'blue', label = 'Исходная функция')
plt.axis('equal')
plt.plot(ts, imsg, c = 'red', linestyle = '--', label = 'Част. сумма ряда Фурье')
plt.axis('equal')
plt.draw()
plt.ioff()

plt.xlabel("t")
plt.ylabel("Re(f(t))")
plt.legend()
plt.grid()
plt.show()
for N in [1, 2, 3, 5, 10]:
    k = -1 * N
    ns = []
    cns = []
    for p in range(2 * N + 1):
        ns.append(k)
        cns.append(cn(k))
        k = k + 1
    s = 0
    for c in cns:
        csopr = c.real - c.imag * i
        s = s + c * csopr
    pars = 8 * s
    print(pars)
