%% Acquire Data in the Foreground
%create session object
s = daq.createSession('ni');
%Set acquisition duration
s.DurationInSeconds = 0.3;
s.Rate = 20000;

%add analog input channel
addAnalogInputChannel(s,'Dev12','ai1','Voltage');
addAnalogInputChannel(s,'Dev12','ai2','Voltage');
ch = addAnalogInputChannel(s,'Dev12','ai3','Voltage');
ch.Range = [-1, 1];

%get data
 c0 = 19; %Tamb, cambiar antes de medir
 c1 = 2.5173462 * 10^1;
 c2 = -1.1662878;
 c3 = -1.0833638;
 c4 = -8.9773540 * 10^-1;
data = startForeground(s);
V = data(:,3).*1000;
T = c0 + c1*V + c2*V.^2 + c3*V.^3 + c4*V.^4;
data(:,3) = T;
data(:,4) = V;
%('Primario Volts' 'Secundario Volts' 'Thermo C' 'Voltaje thermo');
% figure(1)
% plot(data);
% hold on
% figure(2)
% plot(data(:,1), data(:,2))
% hold off
t = mean(T);
mT = strrep(num2str(mean(T),3),'.','x');
archivo = strcat(datestr(now,'dd-mmmm-yyyy_HH-MM-SS_'),'T',mT);
%save(archivo, 'data');
csvwrite(strcat(archivo,'.csv'), data);
disp(mT);
%% GUARDAR
archivo = strcat(datestr(now,'dd-mmmm-yyyy_HH-MM-SS_'));
save(archivo, 'data');
%%
 csvwrite('matrox.csv', data);
%%MEDIR TEMP
s = daq.createSession('ni');
%Set acquisition duration
s.DurationInSeconds = 0.3;
s.Rate = 20000;
ch = addAnalogInputChannel(s,'Dev12','ai3','Voltage');
ch.Range = [-1, 1];
c0 = 0;

 c1 = 2.5173462 * 10^1;

 c2 = -1.1662878;

 c3 = -1.0833638;
 
 c4 = -8.9773540 * 10^-1;
data = startForeground(s);
V = data(:).*1000;
T = c0 + c1*V + c2*V.^2 + c3*V.^3 + c4*V.^4;
data(:) = T;
mean(T);
%%
archivo_de_datos = strcat(datestr(now,'dd-mmmm-yyyy_HH-MM-SS_'),'.csv');       %crea el nombre del archivo de datos
    FILE = fopen(archivo_de_datos,'at');
    fprintf(FILE,'%s','  Canal;  Tiempo1;  Valor1;  Canal; Tiempo2;  Valor2;  Canal; Tiempo3;  Valor3;  Canal; Tiempo4;  Valor4; Canal; Tiempo5;  Valor5; Canal; Tiempo6;  Valor6; Canal; Tiempo7;  Valor7' );
    fprintf(FILE,'\n');
  
    fprintf(FILE,'%f;',data(:,1));
    fprintf(FILE,'%f;',data(:,2));
    fprintf(FILE,'%f\n',data(:,3));
   
%%

%set duration and rate
s.DurationInSeconds = 2;
s.Rate = 10000;


%get data
data =  startForeground(s);
%plot measured data
plot (diff(data(:,1)))