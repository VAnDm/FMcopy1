
T = 30; % Большой интервал времени
dt = 0.01; % Маленький шаг дискретизации
t = -T/2 : dt : T/2; % Набор временный шагов
V = 1/dt; % Ширина диапазона частот
dv = 1/T; % Шаг частоты
v = -V/2 : dv : V/2; % Набор частот для FFT

t_1 = -pi;
t_2 = pi;
a = 3;

g = zeros(size(t));
g(t >= t_1 & t <= t_2) = a; % Значения функции g(t)
xi = 2*rand(size(t)) - 1; % Дискретные значения шума

b = 1;
c = 0.8;
d = 50;

width = 800;
height = 600;
resolution = 300;

u = g + b*xi + c*sin(d*t);

figure;
plot(t, u, 'LineWidth', 1.5);
grid on;
xlim([-T/2-1 T/2+1]);
ylim([-1.5 5]);
xlabel("t", FontSize=24);
ylabel("u(t)", FontSize=24);
title("Зашумлённая g(t)", FontSize=24);


set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'noise_g.png', 'Resolution', 300);


figure;
plot(t, g, 'LineWidth', 1.5);
grid on;
ylim([-1.5 5]);
xlim([-T/2-1 T/2+1]);
xlabel("t", FontSize=24);
ylabel("g(t)",FontSize=24);
title("Функция g(t)", FontSize=24);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'function_g.png', 'Resolution', 300);


U = fftshift(fft(u));

figure;
plot(v, abs(U), 'LineWidth', 1.5);
grid on;
ylim([-5 2000]);
xlim([-V/2-1 V/2+1]);
xlabel("v", FontSize=24);
ylabel("U(v)",FontSize=24);
title("Фурье-образ функции u(t)", FontSize=24);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'im_noise.png', 'Resolution', 300);

