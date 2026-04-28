T = 4; % Большой интервал времени
dt = 0.01; % Маленький шаг дискретизации
t = -T/2 : dt : T/2; % Набор временный шагов
V = 1/dt; % Ширина диапазона частот
dv = 1/T; % Шаг частоты
v = -V/2 : dv : V/2;

p = zeros(size(t));
p(t >= -1/2 & t <= 1/2) = 1;
p_f = (exp(-1i*pi*v) - exp(1i*pi*v)) ./ (-2*1i*pi*v);
p_f(v == 0) = 1;
figure;
plot(v, real(p_f), 'b', v, imag(p_f), 'r--', 'LineWidth', 1.5);
%plot(v, p_f, LineWidth=1.5);
grid on;
ylim([-0.4 1.2]);
xlim([-V/2 V/2]);
xlabel("t", FontSize=24);
ylabel("p(t)",FontSize=24);
legend('p(t)');
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
%exportgraphics(gcf, 'fur_pi_true.png', 'Resolution', 300);


%% Настройка параметров (по 3 значения для каждого)
T_vals = [2, 4, 8];       % Интервал времени
V_vals = [50, 100, 200];  % Диапазон частот
dt_vals = [0.01, 0.02, 0.05]; % Шаг по времени
dv_vals = [0.1, 0.2, 0.5];    % Шаг по частоте

% Создание директории для сохранения
outDir = fullfile('Paper', 'images');
if ~exist('Paper', 'dir'), mkdir('Paper'); end
if ~exist(outDir, 'dir'), mkdir(outDir); end

%% Перебор комбинаций
comboCount = 0;
totalCombos = numel(T_vals) * numel(V_vals) * numel(dt_vals) * numel(dv_vals);

for T = T_vals
    for V = V_vals
        for dt = dt_vals
            for dv = dv_vals
                comboCount = comboCount + 1;
                fprintf('Обработка комбинации %d из %d...\n', comboCount, totalCombos);
                
                % 1. Сетки
                t = -T/2 : dt : T/2;
                v = -V/2 : dv : V/2;
                
                % 2. Исходный сигнал
                p = double(abs(t) <= 0.5); % Прямоугольный импульс
                
                % 3. Аналитический спектр
                p_f = (exp(-1i*pi*v) - exp(1i*pi*v)) ./ (-2*1i*pi*v);
                p_f(abs(v) < dv/2) = 1; % Робастная обработка нуля
                
                % 4. Прямое численное Фурье-преобразование (trapz)
                ker = exp(-2*pi*1i * v.' * t);       % Nv x Nt
                integrand = p .* ker;                % 1 x Nt .* Nv x Nt -> Nv x Nt
                trap_im = trapz(t, integrand, 2);    % Интегрирование по t (столбцы) -> Nv x 1
                
                % 5. Обратное численное Фурье-преобразование (trapz)
                ker2 = exp(2*pi*1i * v.' * t);       % Nv x Nt
                integrand_inv = trap_im .* ker2;     % Nv x 1 .* Nv x Nt -> Nv x Nt
                p_rev = trapz(v, integrand_inv, 1);  % Интегрирование по v (строки) -> 1 x Nt
                
                % 6. Визуализация
                fig = figure('Visible', 'off');
                set(fig, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
                
                % Сравнение сигналов
                subplot(1, 2, 1);
                plot(t, p, 'b', 'LineWidth', 1.5); hold on;
                plot(t, real(p_rev), 'r--', 'LineWidth', 1.5);
                grid on;
                xlabel('t', 'FontSize', 16); ylabel('p(t)', 'FontSize', 16);
                legend('Истинная', 'Восстановленная (trapz)', 'Location', 'best');
                title(sprintf('Сигнал: T = %.1f, dt = %.3f', T, dt), 'FontSize', 14);
                ylim([-0.2 1.2]); xlim([-T/2 T/2]);
                
                % Сравнение спектров
                subplot(1, 2, 2);
                plot(v, real(p_f), 'b', 'LineWidth', 1.5); hold on;
                plot(v, real(trap_im), 'r--', 'LineWidth', 1.5);
                grid on;
                xlabel('v', 'FontSize', 16); ylabel('F(v)', 'FontSize', 16);
                legend('Истинный', 'Численный (trapz)', 'Location', 'best');
                title(sprintf('Спектр: V = %.0f, dv = %.2f', V, dv), 'FontSize', 14);
                ylim([-0.4 1.2]); xlim([-V/2 V/2]);
                
                % 7. Сохранение
                fname = sprintf('T%.1f_V%.0f_dt%.3f_dv%.2f.png', T, V, dt, dv);
                exportgraphics(fig, fullfile(outDir, fname), 'Resolution', 300);
                close(fig);
            end
        end
    end
end
fprintf('✅ Готово! Все %d графиков сохранены в %s\n', totalCombos, outDir);

