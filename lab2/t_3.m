
[y, fs] = audioread("Аккорд (17).mp3");
t = (0:length(y)-1) / fs;  
t = t(:);
%figure;
%plot(t, y(:, 1));        

%xlabel('t')
%ylabel('f(t)')
%title('График амплитуды из файла')
V = 2200;
dv = 0.1;
y = y(:, 1);
y = y(:);
v = 0 : dv : V;
Y = zeros(size(v));

for k = 1 : length(v)
    Y(k)=trapz(t,y.*exp(-1i*2*pi*v(k)*t));
end

figure;

plot(v, abs(Y), 'LineWidth',1.5); 
xlabel('w')
ylabel('f(w)')
title('Фурье образ для амплитуд аккорда')