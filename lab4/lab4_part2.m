width = 800;
height = 600;
resolution = 300;
a = 1;
t1 = 0;
t2 = 2*pi;
N = 500;
b = 0;
c = 0.5;
d = 10;
dt = 0.1;
Fs = 1/dt;
T = N*dt; 
t = (-T/2 : dt : T/2-dt)';

f_Hz = (0:N-1)' * Fs/N; 
omega = 2*pi * f_Hz;
momega = 2*pi*(N-1)*Fs/N;
norm_omega = (-momega/2 : 2*pi*Fs/N : momega/2);

%T_arr = [0.1, 0.5, 1.25, 2.0];
a1 = 0;
a2 = 25;
b1 = 25;
b2 = 25;
%a_arr = [1.0, 2.0, 7.5, 10.0];


xi = -1 + 2 * rand(N, 1);
g = zeros(size(t));
g((t >= t1 & t <= t2)) = a;
y = g + b*xi + c * sin(d * t);

w = tf([1, a1, a2], [1, b1, b2]);
    
figure;
[amp, ~, wout] = bode(w);
amp = squeeze(amp);
plot(wout, amp, 'LineWidth', 1.5);
grid on;
ylim([0 1.1]);
xlim([0 10]);
xlabel("w", FontSize=24);
ylabel("W(iw)",FontSize=24);
title("АЧХ динамического фильтра при b1 = " + b1, FontSize=24);
legend("АЧХ динамического фильтра b1 = " + b1, 'Location', 'northeast', fontsize=18);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "filter_ach_b1_" + b1 + ".png", 'Resolution', 300);
    
w_d = c2d(w, dt, 'foh');
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
title("Фильтрация сигнала при b1 = " + b1, FontSize=24);
legend("Оригинал", "Зашумлённая функция", "Фильтрованная функция",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "filter_b1_" + b1 + ".png", 'Resolution', 300);

figure;
plot(t, y_fil, 'LineWidth', 3.5, color="green");
hold on;
plot(t, y_fil_rev, 'LineWidth', 1.0, color="red");
hold off;
grid on;
xlabel("t", FontSize=24);
ylabel("y(t)",FontSize=24);
title("Сравнение сигналов при b1 = " + b1, FontSize=24);
legend("lsim (временной)", "ifft (частотный)",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "filter_transf_b1_" + b1 + ".png", 'Resolution', 300);

figure;
plot(norm_omega, abs(y_fur), 'LineWidth', 1.5, color="blue");
hold on;
plot(norm_omega, abs(g_fur), 'LineWidth', 0.5, color="red");
hold on;
plot(norm_omega, abs(fil_fur), 'LineWidth', 1.0, color="green");
hold off;
grid on;
ylim([-1.5 50.5]);
xlim([-momega/2 momega/2]);
xlabel("w", FontSize=24);
ylabel("y(w)",FontSize=24);
title("Сравнение фурье-образов при b1 = " + b1, FontSize=24);
legend("Образ зашумлённой функции", "Образ исходной функции", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "fur_imgs_g_b1_" + b1 + ".png", 'Resolution', 300);

figure;
plot(norm_omega, abs(fil_fur), 'LineWidth', 3.5, color="green");
hold on;
plot(norm_omega, abs(Y_fur_plot), 'LineWidth', 1.0, color="red");
hold off;

grid on;
ylim([-1.5 50.5]);
xlim([-momega/2 momega/2]);
xlabel("w", FontSize=24);
ylabel("y(w)",FontSize=24);
title("Сравнение фурье-образов при b1 = " + b1, FontSize=24);
legend("Умножение на передаточную функцию", "Образ фильтрованной функции",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "fur_imgs_w_b1_" + b1 + ".png", 'Resolution', 300);
