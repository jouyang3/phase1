clear; close all;

mu=1;
lambda=[0.1 0.25 0.4 0.55 0.65 0.8 0.9];
ro=lambda./mu;
N=ro.^2./(1-ro);


phase1p1 = csvread('statsp1.csv');
phase1p1ec = csvread('statsp1ec.csv');

phase1p3 = csvread('statsp3.csv');
phase1p3ec = csvread('statsp3ec.csv');


% Average queue length
sim_N = phase1p1(:,4);

figure;
plot(lambda, N, '--o');
hold on;
plot(lambda, sim_N, '-o');

title('Queue Length vs. Arrival Rate \lambda (\mu = 1)');
xlabel('\lambda');
ylabel('Average Queue Length');
legend('Theoretical','Exp. Exponential')

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('queue_length.png','-dpng');

% Average queue length pareto
sim_Nec = phase1p1ec(:,4);

figure;
plot(lambda*10, sim_Nec, '-.o');

title('Queue Length vs. Rate \alpha (\mu = 1)');
xlabel('\alpha');
ylabel('Average Queue Length');

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('queue_length_ec.png','-dpng');

% Utilization

sim_ro = phase1p1(:,5);

figure;
plot(lambda, ro, '--o');
hold on;
plot(lambda, sim_ro, '-o');

title('Utilitation vs. Arrival Rate \lambda (\mu = 1)');
xlabel('\lambda');
ylabel('Utilization Factor');
legend('Theoretical','Experimental Exponential')

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('utilization.png','-dpng');


% Utilization pareto

sim_roec = phase1p1ec(:,5);

figure;
plot(lambda*10, sim_roec, '-.o');

title('Utilitation vs. Rate \alpha (\mu = 1)');
xlabel('\alpha');
ylabel('Utilization Factor');

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('utilization_ec.png','-dpng');




% dropped packets

dropped_1 = phase1p3(1:5,6)';
dropped_20 = phase1p3(6:10,6)';
dropped_50 = phase1p3(11:15,6)';

lambda = [0.2 0.4 0.6 0.8 0.9];

figure;
plot(lambda, dropped_1, '-o');
hold on;
plot(lambda, dropped_20, '--o');
plot(lambda, dropped_50, '.-o');


title('Dropped Packets vs. Arrival Rate \lambda (\mu = 1)');
xlabel('\lambda');
ylabel('Dropped Packets');
legend('1 element queue', '20 element queue', '50 element queue');

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('packets_dropped.png','-dpng');

% Dropped pareto

dropped_1ec = phase1p3(1:5,6)';
dropped_20ec = phase1p3(6:10,6)';
dropped_50ec = phase1p3(11:15,6)';

figure;
plot(lambda*10, dropped_1ec, '-o');
hold on;
plot(lambda*10, dropped_20ec, '--o');
plot(lambda*10, dropped_50ec, '.-o');


title('Dropped Packets vs. Arrival Rate \alpha (\mu = 1)');
xlabel('\alpha');
ylabel('Dropped Packets');
legend('1 element queue', '20 element queue', '50 element queue');

set(gcf,'PaperUnits','inches','PaperPosition',[0 0 8 6])
set(gcf,'visible','off');
print('packets_dropped_ec.png','-dpng');
