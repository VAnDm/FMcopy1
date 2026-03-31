
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

b = 0.5;
c = 0.5;
d = 20;

width = 800;
height = 600;
resolution = 300;

u = g + b*xi + c*sin(d*t);




U = fftshift(fft(u));
G = fftshift(fft(g));


%low_filter = zeros(size(v));
%low_filter((v >= -8 & v <= -3.5) | (v >= -2.5 & v <= 2.5) | (v >= 3.5 & v <= 8)) = 1;
%low_filter(v >= -1 & v <= 1) = 1;
low_filter = ones(size(v));
low_filter(v >= -1 & v <= 1) = 0;


hi_fil_u = U .* low_filter;

figure;
plot(v, abs(U), 'LineWidth', 1.5, 'Color', 'cyan');
hold on;
plot(v, abs(hi_fil_u), 'LineWidth', 1.5, 'Color', 'red');
hold on;
plot(v, abs(G), '--g', 'LineWidth', 1.5, 'Color', 'black')
grid on;
ylim([-5 300]);
xlim([-10 10]);
xlabel("v", FontSize=24);
ylabel("F_i(v)",FontSize=24);
legend('F[u](v)', "F[u]_fil(v)", "F[g](v)");
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'furhigh1.png', 'Resolution', 300);

filtered_g = ifft(ifftshift(hi_fil_u));

figure;
plot(t, u, 'LineWidth', 1.5, 'Color', 'cyan');
hold on;
plot(t, filtered_g, 'LineWidth', 1.5, 'Color', 'red');
hold on;
plot(t, g, 'LineWidth', 1.5, 'Color', 'black');
hold on;
grid on;
ylim([-1.5 4]);
xlim([-T/2-1 T/2+1]);
xlabel("t", FontSize=24);
ylabel("g_i(t)",FontSize=24);
legend('u(t)', "u_fil(t)", "g(t)");
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'grhigh1.png', 'Resolution', 300);


