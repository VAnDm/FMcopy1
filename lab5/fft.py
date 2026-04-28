import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры (по вашему ТЗ)
T_vals = [2, 4, 8]
V_vals = [50, 100, 200]   # В БПФ фактический диапазон частот = 1/(2*dt)
dt_vals = [0.01, 0.03, 0.05]
dv_vals = [0.001, 0.25, 0.5] # В БПФ фактический шаг частоты = 1/T

# Формируем список комбинаций
combos = []
for i in range(len(T_vals)):
    combos.append((T_vals[i], V_vals[i], dt_vals[0], dv_vals[0]))
for i in range(len(T_vals)):
    combos.append((T_vals[i], V_vals[i], dt_vals[-1], dv_vals[-1]))
mid = len(T_vals) // 2
combos.append((T_vals[mid], V_vals[mid], dt_vals[mid], dv_vals[mid]))
combos = list(dict.fromkeys(combos))

out_dir = os.path.join('lab5', 'Paper', 'images')
os.makedirs(out_dir, exist_ok=True)

for idx, (T, V, dt, dv) in enumerate(combos, 1):
    print(f"[{idx}/{len(combos)}] T={T}, V={V}, dt={dt}, dv={dv}")

    # 1. Временная сетка
    Nt = int(T / dt) + 1
    t = np.linspace(-T/2, T/2, Nt)
    dt_actual = dt  # точный шаг (страховка от ошибок округления)

    # 2. Исходный сигнал
    p = np.where(np.abs(t) <= 0.5, 1.0, 0.0)

    # 3. Прямое БПФ
    # 🔑 Масштабирование: умножаем на dt, чтобы аппроксимировать непрерывный интеграл
    F_fft = np.fft.fftshift(np.fft.fft(p)) * dt_actual
    # Частотная сетка БПФ (циклы в секунду, совпадает с определением через 2πivt)
    v_fft = np.fft.fftshift(np.fft.fftfreq(Nt, d=dt_actual))

    # 4. Аналитический спектр (вычисляем на той же сетке v_fft для честного сравнения)
    p_f = np.sinc(v_fft)  # np.sinc(x) = sin(πx)/(πx), уже корректна в 0

    # 5. Обратное БПФ
    # 🔑 Делим на dt перед ifft, чтобы компенсировать прямое масштабирование
    p_rec = np.fft.ifft(np.fft.ifftshift(F_fft / dt_actual))
    p_rec = np.real(p_rec)  # отбрасываем машинный шум (~1e-16j)

    # 📊 Диагностика
    max_rec = np.max(p_rec)
    print(f"   Max восст.: {max_rec:.4f} | Ошибка: {abs(max_rec-1):.2%}")
    print(f"   🔍 Реальная сетка БПФ: dv_real={1/T:.4f}, V_real={1/(2*dt_actual):.1f}")

    # 6. График сигнала
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(t, p, 'b-', linewidth=1.5, label='Истинная')
    ax1.plot(t, p_rec, 'r--', linewidth=1.5, label='Восстановленная (FFT)')
    ax1.set_xlabel('t', fontsize=16); ax1.set_ylabel('p(t)', fontsize=16)
    ax1.set_title(f'Сигнал: T={T}, dt={dt}', fontsize=14)
    ax1.legend(loc='best', fontsize=12); ax1.grid(True)
    ax1.set_ylim([-0.2, 1.3])
    ax1.set_xlim([-T/2, T/2])
    fname1 = f"FFT_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_signal.png"
    fig1.savefig(os.path.join(out_dir, fname1), dpi=300, bbox_inches='tight')
    plt.close(fig1)

    # 7. График спектра
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(v_fft, np.real(p_f), 'b-', linewidth=1.5, label='Истинный')
    ax2.plot(v_fft, np.real(F_fft), 'r--', linewidth=1.5, label='Численный (FFT)')
    ax2.set_xlabel('v', fontsize=16); ax2.set_ylabel('F(v)', fontsize=16)
    ax2.set_title(f'Спектр: V={V}, dv={dv}', fontsize=14)
    ax2.legend(loc='best', fontsize=12); ax2.grid(True)
    ax2.set_ylim([-0.4, 1.5])
    ax2.set_xlim([-v_fft[-1], v_fft[-1]]) # масштаб по реальной частоте Найквиста
    fname2 = f"FFT_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_spectrum.png"
    fig2.savefig(os.path.join(out_dir, fname2), dpi=300, bbox_inches='tight')
    plt.close(fig2)

print(f"✅ Готово! Все графики сохранены в {out_dir}")