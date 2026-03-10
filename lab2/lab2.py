import numpy as np
import matplotlib.pyplot as plt

def g(t, c):
    return 2*np.exp(-(t+c)**2/2)

def g_fur_im(t, c):
    g = 2*np.exp(1.j*t*c)*np.exp(-t**2/2)
    return np.abs(g), g.real, g.imag


cs = [-1, -1/np.pi, np.pi, 4]
t = np.linspace(-8, 8, 2000)


for c in cs:
    g_orig, re, im = g_fur_im(t, c)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('w', fontsize=12)
    ax.set_ylabel('g(w)', fontsize=12)
    
    ax.set_title(f'Фурье-образ', fontsize=14)
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-7, 7)
    ax.axis("on")
    ax.axhline(y=0, color='k', alpha=0.1)
    ax.axvline(x=0, color='k', alpha=0.1) 
    ax.grid(True, alpha=0.3)
    
    ax.plot(t, g_orig, linewidth=1.5, label=f'Фурье-образ функции со сдвигом c = {round(c,3)}')
    ax.legend(loc='upper left', fontsize=10)

    filename = f"t2_fur_{round(c, 3)}.png"

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('w', fontsize=12)
    ax.set_ylabel('Re(g(w)), Im(g(w))', fontsize=12)
    
    ax.set_title(f'Мнимая и действительная части Фурье-образа', fontsize=14)
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-7, 7)
    ax.axis("on")
    ax.axhline(y=0, color='k', alpha=0.1)
    ax.axvline(x=0, color='k', alpha=0.1) 
    ax.grid(True, alpha=0.3)
    
    
    ax.plot(t, re, linewidth=1.5, label=f'Действительная часть Фурье-образа')
    ax.plot(t, im, linewidth=1.5, label=f'Мнимая часть Фурье-образа')
    ax.legend(loc='upper left', fontsize=10)
    
    filename = f"t2_reim_{round(c, 3)}.png"

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close(fig)