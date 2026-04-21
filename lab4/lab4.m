width = 800;
height = 600;
resolution = 300;
a = 1;
t1 = 0;
t2 = 2*pi;
N = 500;
b = 0.5;
dt = 0.1;
Fs = 1/dt;
T = N*dt; 
t = (-T/2 : dt : T/2-dt)';

f_Hz = (0:N-1)' * Fs/N; 
omega = 2*pi * f_Hz;

T_arr = [0.1, 0.5, 1.25, 2.0];
a_arr = [1.0, 2.0, 7.5, 10.0];


for i = 1:length(T_arr)
    xi = -1 + 2 * rand(N, 1);
    g = zeros(size(t));
    g((t >= t1 & t <= t2)) = a;
    y = g + b*xi;

    T_c = T_arr(i);
    w = tf(1, [T_c, 1]);
    
    figure;
    [amp, ~, wout] = bode(w);
    amp = squeeze(amp);
    plot(wout, amp, 'LineWidth', 1.5);
    grid on;
    ylim([0 1.1]);
    xlim([0 10]);
    xlabel("w", FontSize=24);
    ylabel("W(iw)",FontSize=24);
    title("АЧХ динамического фильтра при T = " + T_c, FontSize=24);
    legend("АЧХ динамического фильтра T = " + T_c, 'Location', 'northeast', fontsize=18);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_ach_T_" + T_c + ".png", 'Resolution', 300);
    
    w_d = c2d(w, dt, 'zoh');
    [H_d, ~] = freqz(w_d.Num{1}, w_d.Den{1}, N, 'whole');
    
    Y = fft(y);
    H_d = H_d(:);  % Явно делаем столбцом
    Y = Y(:);
    y_fil_rev = real(ifft(Y .* H_d));
    
    y_fil = lsim(w, y, t);
    
    y_fur = fftshift(fft(y));
    g_fur = fftshift(fft(g));
    fil_fur = fftshift(fft(y_fil));
    Y_fur_plot = fftshift(Y .* H_d);

    figure;
    plot(t, g, 'LineWidth', 3.5, color="blue");
    hold on;
    plot(t, y, 'LineWidth', 0.5, color="red");
    hold on;
    plot(t, y_fil, 'LineWidth', 3.5, color="green");
    hold off;
    grid on;
    ylim([-0.5 1.5]);
    xlim([-T/2 T/2]);
    xlabel("t", FontSize=24);
    ylabel("y(t)",FontSize=24);
    title("Фильтрация сигнала при T = " + T_c, FontSize=24);
    legend("Оригинал", "Зашумлённая функция", "Фильтрованная функция",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_T_" + T_c + ".png", 'Resolution', 300);

    figure;
    plot(t, y_fil, 'LineWidth', 1.25, color="blue");
    hold on;
    plot(t, y_fil_rev, 'LineWidth', 1.25, color="red");
    hold off;
    grid on;
    xlabel("t", FontSize=24);
    ylabel("y(t)",FontSize=24);
    title("Сравнение сигналов при T = " + T_c, FontSize=24);
    legend("lsim (временной)", "ifft (частотный)",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_transf_T_" + T_c + ".png", 'Resolution', 300);

    figure;
    plot(omega, abs(y_fur), 'LineWidth', 1.0, color="blue");
    hold on;
    plot(omega, abs(g_fur), 'LineWidth', 0.5, color="red");
    hold on;
    plot(omega, abs(fil_fur), 'LineWidth', 1.0, color="green");
    hold off;
    grid on;
    ylim([-1.5 50.5]);
    xlim([0 63]);
    xlabel("w", FontSize=24);
    ylabel("y(w)",FontSize=24);
    title("Сравнение фурье-образов при T = " + T_c, FontSize=24);
    legend("Образ зашумлённой функции", "Образ исходной функции", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "fur_imgs_g_T_" + T_c + ".png", 'Resolution', 300);

    figure;
    plot(omega, abs(Y_fur_plot), 'LineWidth', 0.5, color="red");
    hold on;
    plot(omega, abs(fil_fur), 'LineWidth', 1.0, color="blue");
    hold off;
    grid on;
    ylim([-1.5 50.5]);
    xlim([0 63]);
    xlabel("w", FontSize=24);
    ylabel("y(w)",FontSize=24);
    title("Сравнение фурье-образов при T = " + T_c, FontSize=24);
    legend("Умножение на передаточную функцию", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "fur_imgs_w_T_" + T_c + ".png", 'Resolution', 300);

    a_c = a_arr(i);
    xi = -1 + 2 * rand(N, 1);
    
    g = zeros(size(t));
    g((t >= t1 & t <= t2)) = a_c;
    y = g + b*xi;

    w = tf(1, [1.1, 1]);
    
    figure;
    [amp, ~, wout] = bode(w);
    amp = squeeze(amp);
    plot(wout, amp, 'LineWidth', 1.5);
    grid on;
    ylim([0 1]);
    xlim([0 10]);
    xlabel("w", FontSize=24);
    ylabel("W(iw)",FontSize=24);
    title("АЧХ динамического фильтра при a = " + a_c + ", T = 1.25", FontSize=24);
    legend("АЧХ динамического фильтра a = " + a_c, 'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_ach_a_" + a_c + ".png", 'Resolution', 300);

    w_d = c2d(w, dt, 'zoh');
    [H_d, ~] = freqz(w_d.Num{1}, w_d.Den{1}, N, 'whole');
    
    Y = fft(y);
    H_d = H_d(:);
    Y = Y(:);
    y_fil_rev = real(ifft(Y .* H_d));
    
    y_fil = lsim(w, y, t);
    
    y_fur = fftshift(fft(y));
    g_fur = fftshift(fft(g));
    fil_fur = fftshift(fft(y_fil));
    Y_fur_plot = fftshift(Y .* H_d);

    figure;
    plot(t, y_fil, 'LineWidth', 1.0, color="blue");
    hold on;
    plot(t, y_fil_rev, 'LineWidth', 1.0, color="red");
    hold off;
    grid on;
    xlabel("t", FontSize=24);
    ylabel("y(t)",FontSize=24);
    title("Сравнение сигналов при a = " + a_c + ", T = 1.25", FontSize=24);
    legend("lsim (временной)", "ifft (частотный)",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_transf_a_" + a_c + ".png", 'Resolution', 300);
    
    figure;
    plot(t, g, 'LineWidth', 3.5, color="blue");
    hold on;
    plot(t, y, 'LineWidth', 0.5, color="red");
    hold on;
    plot(t, y_fil, 'LineWidth', 3.5, color="green");
    hold off;
    grid on;
    ylim([-0.5 a_c+1]);
    xlim([-T/2 T/2]);
    xlabel("t", FontSize=24);
    ylabel("y(t)",FontSize=24);
    title("Фильтрация сигнала при a = " + a_c + ", T = 1.25", FontSize=24);
    legend("Оригинал", "Зашумлённая функция", "Фильтрованная функция",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "filter_a_" + a_c + ".png", 'Resolution', 300);
    
    figure;
    plot(omega, abs(y_fur), 'LineWidth', 1.0, color="blue");
    hold on;
    plot(omega, abs(g_fur), 'LineWidth', 0.5, color="red");
    hold on;
    plot(omega, abs(fil_fur), 'LineWidth', 1.0, color="green");
    hold off;
    grid on;
    ylim([-1.5 50.5]);
    xlim([0 63]);
    xlabel("w", FontSize=24);
    ylabel("y(w)",FontSize=24);
    title("Сравнение фурье-образов при a = " + a_c + ", T = 1.25", FontSize=24);
    legend("Образ зашумлённой функции", "Образ исходной функции", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "fur_imgs_g_a_" + a_c + ".png", 'Resolution', 300);

    figure;
    plot(omega, abs(Y_fur_plot), 'LineWidth', 0.5, color="red");
    hold on;
    plot(omega, abs(fil_fur), 'LineWidth', 1.0, color="blue");
    hold off;
    grid on;
    ylim([-1.5 50.5]);
    xlim([0 63]);
    xlabel("w", FontSize=24);
    ylabel("y(w)",FontSize=24);
    title("Сравнение фурье-образов при a = " + a_c + ", T = 1.25", FontSize=24);
    legend("Умножение на передаточную функцию", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
    set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
    exportgraphics(gcf, "fur_imgs_w_a_" + a_c + ".png", 'Resolution', 300);
end