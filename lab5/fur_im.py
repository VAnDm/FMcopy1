import numpy as np
import matplotlib.pyplot as plt
import os

t = np.linspace(-2, 2, 1000)

f = np.where(np.abs(t) <= 0.5, 1.0, 0.0)

out_dir = os.path.join('lab5', 'Paper', 'images')
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(t, f, 'b-', linewidth=1.5, label="Квадратная волна")
#ax1.plot(t, p_rec, 'r--', linewidth=1.5, label='Восстановленная (FFT)')
ax1.set_xlabel('t', fontsize=16); ax1.set_ylabel('p(t)', fontsize=16)
ax1.set_title(f'Квадратная волна', fontsize=14)
ax1.legend(loc='best', fontsize=16); ax1.grid(True)
ax1.set_ylim([-0.1, 1.2])
ax1.set_xlim([-2, 2])
fname1 = f"pi_true.png"
fig1.savefig(os.path.join(out_dir, fname1), dpi=300, bbox_inches='tight')
plt.close(fig1)