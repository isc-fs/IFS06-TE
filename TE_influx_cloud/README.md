# influx_cloud
Github repository to manage oss to cloud data replication, and download/visualization of cloud data.


## influx_to_csv.py
    Permite descargar y visualizar los datos almacenados ya sea en la nube o en local con
    el formato apropiado en su respectivo .csv.

    Actual: 1.4.2



    influx_csv_v1.3.exe
    SOLUCIONADO
        - Variables del .csv estaban como string en el dataframe, conversiones hechas.
        - Ignores 'piloto' and 'circuito' variables when making .csv


    influx_csv_v1.2.exe
        SOLUCIONADO:
            -  En la opcion 2, si introduces un bucket que no existe sale error. Solucionar.
            -  Las visualizaciones estaban fijas en las variables ax,ay,az

## replicate_auto.py
    Permite sincronizar automaticamente los datos almacenados en local (maletin) con la nube (influx cloud)
        - Es un codigo bastante sencillo

## scratches
    Dentro de esta carpeta podemos encontrar o archivos de prueba o funciones que se estan utilizando por otros archivos, cuidado a la hora de manipular.


## NOTAS

https://pypi.org/project/auto-py-to-exe/
Convert .py to .exe using this

python 3.9.2
Estamos usando un range de los ultimos 300d, en algun momento habrá que extender ese periodo.