width = 800;
height = 600;
resolution = 300;

[y,f] = audioread('MUHA.wav');


%sound(y, f);

dt = 1/f; % Шаг времени
T = length(y)*dt; 
t = 0 : dt : T-dt; 
V = 1/dt;
dv = 1/T;
v = -V/2 : dv : V/2-dv;

y_image = fftshift(fft(y));
high_filter = zeros(size(v));
high_filter((v>=-1200 & v <= -400) | (v >= 400 & v <= 1200)) = 1;

figure;
plot(v, abs(y_image), 'LineWidth', 1.5);
hold on;
plot(v, high_filter*1000, 'LineWidth', 2.5, color="red");
hold off;
grid on;
%ylim([-2.5 4]);
%xlim([-V/2-1 V/2+1]);
xlabel("v", FontSize=24);
ylabel("Y(v)",FontSize=24);
title("Фурье-образ звука", FontSize=24);
legend('Фурье-образ звука', 'Режекторный полосовой фильтр', 'Location', 'northeast', fontsize=18);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'fur_muha.png', 'Resolution', 300);

high_filter = high_filter(:);
y_image = y_image(:);

hi_fil_u = y_image .* high_filter;

figure;
plot(v, abs(hi_fil_u), 'LineWidth', 1.5);
grid on;
%ylim([-2.5 4]);
%xlim([-V/2-1 V/2+1]);
xlabel("t", FontSize=24);
ylabel("g'(t)",FontSize=24);
title("Отфильтрованный Фурье-образ звука", FontSize=24);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'filtered_fur_muha.png', 'Resolution', 300);

filtered_y = ifft(ifftshift(hi_fil_u));

sound(filtered_y, f)


figure;
plot(t, y, 'LineWidth', 1.5, color='red');
hold on;
plot(t, filtered_y, 'LineWidth', 1.5, color="blue");
hold off;
grid on;
ylim([-2.5 4]);
%xlim([-V/2-1 V/2+1]);
xlabel("t", FontSize=24);
ylabel("y(t)",FontSize=24);
title("Сравнение отфильтрованного и исходного сигналов", FontSize=24);
legend('Исходный сигнал', 'Отфильтрованный сигнал', 'Location', 'northeast', fontsize=18);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, 'filtered_muha.png', 'Resolution', 300);


