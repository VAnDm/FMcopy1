import numpy as np
import matplotlib.pyplot as plt
import os

# Совместимость с NumPy 2.0+
trapz = getattr(np, 'trapezoid', np.trapz)

# Параметры (исправлен синтаксис: добавлены пропущенные запятые)
T_vals = [2, 4, 8]
V_vals = [50, 100, 200]  # Исправлено: добавлена запятая (предполагаю 100 вместо 32)
dt_vals = [0.01, 0.01, 0.05]
dv_vals = [0.001, 0.1, 0.5]

out_dir = os.path.join('lab5', 'Paper', 'images')
os.makedirs(out_dir, exist_ok=True)

# 🔑 Формируем список ТОЛЬКО нужных комбинаций
combos = []

# 1. Соответствующие пары (T, V) с первыми dt и dv
for i in range(len(T_vals)):
    combos.append((T_vals[i], V_vals[i], dt_vals[0], dv_vals[0]))

# 2. Соответствующие пары (T, V) с последними dt и dv
for i in range(len(T_vals)):
    combos.append((T_vals[i], V_vals[i], dt_vals[-1], dv_vals[-1]))

# 3. Срединная комбинация
mid = len(T_vals) // 2
combos.append((T_vals[mid], V_vals[mid], dt_vals[mid], dv_vals[mid]))

# Убираем возможные дубликаты, сохраняя порядок
combos = list(dict.fromkeys(combos))

total_combos = len(combos)
print(f"📋 Сгенерировано комбинаций для обработки: {total_combos}")
for c in combos:
    print(f"   T={c[0]:>2}, V={c[1]:>3}, dt={c[2]:.3f}, dv={c[3]:.3f}")
print("-" * 40)

for idx, (T, V, dt, dv) in enumerate(combos, 1):
    print(f"[{idx}/{total_combos}] T={T}, V={V}, dt={dt}, dv={dv}")

    # 1. Сетки
    Nt = int(T / dt) + 1
    Nv = int(V / dv) + 1
    t = np.linspace(-T/2, T/2, Nt)
    v = np.linspace(-V/2, V/2, Nv)

    # 2. Исходный сигнал
    p = np.where(np.abs(t) <= 0.5, 1.0, 0.0)

    # 3. Аналитический спектр
    p_f = (np.exp(-1j * np.pi * v) - np.exp(1j * np.pi * v)) / (-2j * np.pi * v)
    p_f[np.abs(v) < dv/2] = 1.0

    # 4. Прямое преобразование
    kernel = np.exp(-2j * np.pi * np.outer(v, t))
    integrand = p[np.newaxis, :] * kernel
    trap_im = trapz(integrand, x=t, axis=1)

    # 5. Обратное преобразование
    kernel2 = np.exp(2j * np.pi * np.outer(v, t))
    integrand_inv = trap_im[:, np.newaxis] * kernel2
    p_rev = trapz(integrand_inv, x=v, axis=0)
    p_rev = np.real(p_rev)  # Отсекаем машинный шум

    # 📊 Диагностика
    max_rec = np.max(p_rev)
    print(f"   Max восст.: {max_rec:.4f} (ошибка: {abs(max_rec-1):.2%})")

    # 6. График сигнала
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(t, p, 'b-', linewidth=1.5, label='Истинная')
    ax1.plot(t, p_rev, 'r--', linewidth=1.5, label='Восстановленная (trapz)')
    ax1.set_xlabel('t', fontsize=16); ax1.set_ylabel('p(t)', fontsize=16)
    ax1.set_title(f'Сигнал: T={T}, dt={dt}', fontsize=14)
    ax1.legend(loc='best', fontsize=12); ax1.grid(True)
    # 🔑 Фиксированный масштаб вместо np.max(p_rev)+0.1, чтобы амплитуда не "прыгала"
    ax1.set_ylim([-0.2, 1.3])  
    ax1.set_xlim([-T/2, T/2])
    fname1 = f"T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_signal.png"
    fig1.savefig(os.path.join(out_dir, fname1), dpi=300, bbox_inches='tight')
    plt.close(fig1)

    # 7. График спектра
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(v, np.real(p_f), 'b-', linewidth=1.5, label='Истинный')
    ax2.plot(v, np.real(trap_im), 'r--', linewidth=1.5, label='Численный (trapz)')
    ax2.set_xlabel('v', fontsize=16); ax2.set_ylabel('F(v)', fontsize=16)
    ax2.set_title(f'Спектр: V={V}, dv={dv}', fontsize=14)
    ax2.legend(loc='best', fontsize=12); ax2.grid(True)
    ax2.set_ylim([-0.4, 1.5]); ax2.set_xlim([-V/2, V/2])
    fname2 = f"T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_spectrum.png"
    fig2.savefig(os.path.join(out_dir, fname2), dpi=300, bbox_inches='tight')
    plt.close(fig2)

print(f"✅ Готово! Все {total_combos*2} графиков сохранены в {out_dir}")