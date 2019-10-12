%% LOCKIN SR830

%inicializo el lockin, conectado con la interfase USB - GPIB
li = gpib('ni',0,11);
%reconoce al generador
% gf = visa('ni','USB0::0x0699::0x0346::C036493::INSTR');
gf = gpib('ni',0,7);
%%
%abre la sesión con lockin
fopen(li);
%abre la sesión Visa de comunicación con el generador de funciones
fopen(gf);

%%
%loop seteando la frecuencia
start = 50284;
stop = 50284.5;
step = 0.1;
FREQ=start:step:stop;
medicion='busco_picos_sec';
nombre = strcat(medicion,'_',num2str(start),'_',num2str(stop),'_',num2str(step,'%2.s'));
%nombre = 'Barrido_50094_50097_0.3_3';
%nombre = cosa_start_stop_step(hz)_numero;
archivo_de_datos = strcat(nombre, datestr(now,'HH-MM-SS_'),'.txt');       %crea el nombre del archivo de datos
FILE = fopen(archivo_de_datos,'at');
fprintf(FILE,'%s',' Frec; X; Y; R; Theta' );
fprintf(FILE,'\n');

%FREQ=50095:0.1:50097;

for i=1:(length(FREQ))
    
    str=sprintf('FREQ %f',FREQ(i));
    fprintf(gf,str);
    pause(10);
    str=query(li, 'SNAP ? 1,2,3,4');%pide las cuatro cosas %X=1, Y=2 ; R=3 , tita=4
    data=str2num(str);
    
    subplot(2,1,1);
    hold on
    plot(FREQ(i),data(3),'.');
    subplot(2,1,2);
    hold on
    plot(FREQ(i),data(4),'.');
    
    fprintf(FILE,'%f',FREQ(i) );
    fprintf(FILE,'%s',' ; ');
    fprintf(FILE,'%f',data(1) );
    fprintf(FILE,'%s',' ; ');
    fprintf(FILE,'%f',data(2) );
    fprintf(FILE,'%s',' ; ');
    fprintf(FILE,'%f',data(3) );
    fprintf(FILE,'%s',' ; ');
    fprintf(FILE,'%f',data(4) );
    fprintf(FILE,'\n');
end

hold off

%%
%cierra la sesión Visa de comunicación con el generador de funciones
fclose(gf);
%cierra la sesión con lockin
fclose(li); 


%%
%Leo x: X=1
str=query(li,'outp ?1');
X=str2double(str);

%Leo Y: Y=2
str=query(li,'outp ?2');
Y=str2double(str);

%Leo el modulo: R=3
str=query(li,'outp ?3');
R=str2double(str);

%Leo el ángulo: tita=4
str=query(li,'outp ?4');
tita=str2double(str);



