# generate_latex_blocks.py
import os

# Параметры
T_vals = [2, 4, 8]
V_vals = [50, 100, 200]   # Среднее значение 100 (вместо 32 для симметрии)
dt_vals = [0.01, 0.03, 0.05]
dv_vals = [0.001, 0.25, 0.5]

# Формируем точный список комбинаций по вашему ТЗ
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

with open('figures.tex', 'w', encoding='utf-8') as f:
    count = 0
    for T, V, dt, dv in combos:
        count += 1
        f.write(f"\\newpage\n")
        f.write(f"\\subsection*{{Комбинация {count}: $T={T}$, $V={V}$, $dt={dt}$, $dv={dv}$}}\n\n")
        
        f.write("\\begin{figure}[H]\n")
        f.write("    \\centering\n")
        f.write(f"    \\includegraphics[width=0.95\\textwidth]{{images/FFT_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_signal.png}}\n")
        f.write(f"    \\caption{{Восстановление сигнала: $T={T}$, $dt={dt}$.}}\n")
        f.write("\\end{figure}\n\n")
        
        f.write("\\begin{figure}[H]\n")
        f.write("    \\centering\n")
        f.write(f"    \\includegraphics[width=0.95\\textwidth]{{images/FFT_T{T}_V{V}_dt{dt:.3f}_dv{dv:.3f}_spectrum.png}}\n")
        f.write(f"    \\caption{{Сравнение спектров: $V={V}$, $dv={dv}$.}}\n")
        f.write("\\end{figure}\n\n")

print(f"✅ Создан файл figures.tex с {count} комбинациями")