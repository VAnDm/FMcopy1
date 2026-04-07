from matplotlib import pyplot as plt
import numpy as np
from numpy import pi, sin, cos, exp, log
from scipy import integrate

# t0 = 1
t0 = 0
t1 = pi**2/5
t2 = pi*1.5

a = 2
b = 8

# T = t2-t0
T = 2*pi

# def f(n):
#     t = (n - t0) % T
#     t = t0 + t
    
#     if t0 <= t < t1:
#         return a
#     elif t1 <= t < t2:
#         return b
#     return 0

def f(x):
    # return abs(sin(x))*exp(cos(x)**3)
    return sin(sin(x))*exp(abs(cos(x))**3)/(2+abs(cos(x)))
    # return sin(cos(x))*abs(sin(x))*exp(sin(x))/(2+cos(x)**3)

def omega_n(n):
    return 2 * np.pi * n / T

def a_n(n):
    if n == 0:
        result, _ = integrate.quad_vec(f, t0, t0 + T)
        return result / T
    
    wn = omega_n(n)
    integrand = lambda x: f(x) * np.cos(wn * x)
    result, _ = integrate.quad_vec(integrand, t0, t0 + T)
    return (2 / T) * result

def b_n(n):
    wn = omega_n(n)
    integrand = lambda x: f(x) * np.sin(wn * x)
    result, _ = integrate.quad_vec(integrand, t0, t0 + T)
    return (2 / T) * result

def c_n(n):
    if n == 0:
        result, _ = integrate.quad_vec(f, t0, t0 + T)
        return result / T
    
    wn = omega_n(n)
    integrand = lambda x: f(x) * np.exp(-1j * wn * x)
    result, _ = integrate.quad_vec(integrand, t0, t0 + T)
    return result/T


def F_n(n, x):
    res = 0
    n += 1

    for i in range(n):
        if i == 0:
            res += a_n(0)
        else:
            wn = omega_n(i)
            res += a_n(i)*cos(wn*x) + b_n(i)*sin(wn*x)
    return res

def G_n(n, x):
    res = 0
    for i in range((-n), n+1):
        wn = omega_n(i)
        res += c_n(i)*exp(1j*wn*x)
    return res.real



N_values = [3, 5, 10, 20, 50] 
t = np.linspace(t0, t0 + 3*T, 2000)
# t = np.linspace(-3*pi, 3*pi, 2000)
x_original = np.array([f(val) for val in t])


N = 50

scal = lambda x: f(x)*f(x)

q, _ = integrate.quad_vec(scal, t0, t0+T)
q = q/T
s_tr = a_n(0)**2
s_c = abs(c_n(0))**2

for i in range(1, N):
    s_tr += (a_n(i)**2+b_n(i)**2)/2
    s_c += abs(c_n(i))**2+abs(c_n(-i))**2    

print(f"Проверка равенства Парсеваля при N = {N}(тригонометрический ряд): {q - s_tr}")
print(f"Проверка равенства Парсеваля при N = {N}(комплексный ряд): {q - s_c.real}")

for num in N_values:
    x_fur = F_n(num, t)
    x_fur2 = G_n(num, t)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(t, x_fur, color="red", linewidth=2, label=f'Частичная сумма триг. ряда (N={num})')
    ax.plot(t, x_fur2, color="yellow", linestyle='--', linewidth=2, label=f'Частичная сумма комп. ряда (N={num})')
    ax.plot(t, x_original, color="blue", linewidth=1.5, label='Исходная функция')
    
    ax.set_xlabel('t', fontsize=12)
    ax.set_ylabel('f(t)', fontsize=12)
    # ax.set_title(f'Ряд Фурье для квадратной волны (N = {num} гармоник)', fontsize=14)
    # ax.set_title(f'Ряд Фурье для чётной переодической функции (N = {num} гармоник)', fontsize=14)
    # ax.set_title(f'Ряд Фурье для нечётной переодической функции (N = {num} гармоник)', fontsize=14)
    ax.set_title(f'Ряд Фурье для ни чётной, ни нечётной переодической функции (N = {num} гармоник)', fontsize=14)
    #ax.set_title(f'Функция квадратной волны', fontsize=14)
    # ax.set_xlim(-3*pi-2, 3*pi+2)
    ax.set_xlim(t0-2, t0+3*T+1)
    ax.set_ylim(-0.75, 1)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    filename = f"t4_{num}.png"
    #filename = f"t1_0.png"
    #plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close(fig)
for i in range(3):
   print(f"Коэффициент a_{i}: {a_n(i)}")
   print(f"Коэффициент b_{i}: {b_n(i)}")
   print(f"Коэффициент c_{i}: {c_n(-i)}")

