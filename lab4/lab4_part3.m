tablica = readtable("SBER_220101_260421.csv");
stoimost = table2array(tablica(:, 5));
dates = table2array(tablica(:, 3));
days = zeros(size(dates));
months = zeros(size(dates));
years = zeros(size(dates));
Datestart = datetime(2022, 1, 3);
Datefinish = datetime(2026, 4, 21);
datesfull = Datestart:Datefinish;
for i = 1:length(dates)
    day = mod(dates(i), 100);
    month = mod(dates(i), 10000) - day;
    year = (dates(i) - day - month) / 10000;
    month = month / 100;
    days(i) = day;
    months(i) = month;
    years(i) = year;
end
dates_new = datetime(years, months, days);
stoimostfull = zeros(size(datesfull));
c = 1;
for i = 1:length(datesfull)
    if datesfull(i) == dates_new(c)
        stoimostfull(i) = stoimost(c);
        c = c + 1;
    else
        a = datenum(dates_new(c)) - datenum(dates_new(c - 1));
        b = datenum(datesfull(i)) - datenum(dates_new(c - 1));
        otn = b / a;
        stoimostfull(i) = stoimost(c - 1) + (stoimost(c) - stoimost(c - 1)) * otn;
    end
end
T = 365;
w1 = tf(1, [T, 1]);
massiv = zeros(size(datesfull));
for i = 1:length(datesfull)
    %massiv(i) = datenum(dates_new(i)) - datenum(dates_new(1));
    massiv(i) = i - 1;
end
stoimostfullnorm = stoimostfull - stoimostfull(1);
stoimostgladnorm = lsim(w1, stoimostfullnorm, massiv);
stoimostglad = stoimostgladnorm + stoimostfull(1);
plot(datesfull, stoimostfull, 'LineWidth', 3.5, color="green");
hold on;
plot(datesfull, stoimostglad, 'LineWidth', 1.5, color="red");
hold off;
grid on;
xlabel("Дата", FontSize=24);
ylabel("Стоимость акции",FontSize=24);
title("T = 365 дней", FontSize=14);
legend("Исходный график", "Сглаженный график",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "task3_" + T + "_1.png", 'Resolution', 300);

plot(datesfull(1:T + 1), stoimostfull(1:T + 1), 'LineWidth', 3.5, color="green");
hold on;
plot(datesfull(1:T + 1), stoimostglad(1:T + 1), 'LineWidth', 1.5, color="red");
hold off;
grid on;
xlabel("Дата", FontSize=24);
ylabel("Стоимость акции",FontSize=24);
title("T = 365 дней", FontSize=14);
legend("Исходный график", "Сглаженный график",  'Location', 'northeast', fontsize=14);
set(gcf, 'Units', 'pixels', 'Position', [100, 100, 1200, 800]);
exportgraphics(gcf, "task3_" + T + "_2.png", 'Resolution', 300);