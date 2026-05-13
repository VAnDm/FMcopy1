import numpy as np
import matplotlib.pyplot as plt
import os

out_dir = os.path.join('lab5', 'Paper', 'images')
os.makedirs(out_dir, exist_ok=True)

dt_t = 0.001
dv_t = 0.001

combos = [[4, 100, 0.01, 0.1], [15, 100, 0.01, 0.1], [4, 200, 0.01, 0.1], [4, 100, 0.1, 0.1], [4, 100, 0.01, 0.5] ]
for idx, (T, V, dt, dv) in enumerate(combos, 1):

    V_t = max(V, 100)
    Nt = int(T / dt) + 1
    Nt_true = int(T / dt_t) + 1
    Nv = int(V / dv) + 1
    Nv_true = int(V / dv_t) + 1
    t = np.linspace(-T/2, T/2, Nt)
    t_true = np.linspace(-T/2, T/2, Nt_true)
    v = np.linspace(-V/2, V/2, Nv)
    v_t = np.linspace(-V_t/2, V_t/2, Nv_true)
    dt_actual = dt 
    

    p = np.where(np.abs(t) <= 0.5, 1.0, 0.0)
    p_t = np.where(np.abs(t_true) <= 0.5, 1.0, 0.0)


    m = np.arange(Nt)
    c_m = dt_actual * ((-1) ** abs(m))*np.exp(-np.pi*1j*m/Nt)
    c_m_shifted = np.fft.fftshift(c_m)


    F_fft = np.fft.fftshift(np.fft.fft(p)*c_m)
    v_fft = np.fft.fftshift(np.fft.fftfreq(Nt, d=dt_actual))

    p_f = np.sinc(v_t) 

    p_rec = np.fft.ifft(np.fft.ifftshift(F_fft) / c_m)
    p_rec = np.real(p_rec)

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(t_true, p_t, 'b-', linewidth=2.5, label='Истинная')
    ax1.plot(t, p_rec, 'r--', linewidth=1.5, label='Восстановленная (FFT)')
    ax1.set_xlabel('t', fontsize=16); ax1.set_ylabel('p(t)', fontsize=16)
    ax1.set_title(f'Сигнал: T={T}, dt={dt}', fontsize=14)
    ax1.legend(loc='best', fontsize=16); ax1.grid(True)
    ax1.set_ylim([-0.2, 1.3])
    ax1.set_xlim([-T/2, T/2])
    fname1 = f"FFTc_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_signal.png"
    fig1.savefig(os.path.join(out_dir, fname1), dpi=300, bbox_inches='tight')
    plt.close(fig1)


    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(v_t, np.real(p_f), 'b-', linewidth=2.5, label='Истинный')
    ax2.plot(v_fft, np.real(F_fft), 'r--', linewidth=1.5, label='Численный (FFT)')
    ax2.set_xlabel('v', fontsize=16); ax2.set_ylabel('F(v)', fontsize=16)
    ax2.set_title(f'Спектр: V={V}, dv={dv}', fontsize=14)
    ax2.legend(loc='best', fontsize=16); ax2.grid(True)
    ax2.set_ylim([-1.0, 1.5])
    ax2.set_xlim([-v_fft[-1], v_fft[-1]])
    fname2 = f"FFTc_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_spectrum.png"
    fig2.savefig(os.path.join(out_dir, fname2), dpi=300, bbox_inches='tight')
    plt.close(fig2)

