# FSgit

This code goes in a raspberry pi 4 with a Nrf24L01 module connected, through which we receive data from the car.
Using python we convert this data and store it in influx.


## influx_cloud/indlux_replicate_cloud.py

    Este código en Python se utiliza para replicar datos de una base de datos InfluxDB OSS a CLOUD. Primero, establece las conexiones a las bases de datos de origen y destino utilizando las credenciales y URLs proporcionadas. Luego, define varias funciones para replicar los datos y crear un nuevo bucket en la base de datos de destino si es necesario.

    La función replicate__ lee los datos de la base de datos de origen, crea puntos de datos a partir de los registros leídos y los escribe en la base de datos de destino. Función desactualiada.

    La función replicate hace lo mismo que replicate__, pero también convierte la marca de tiempo de cada registro a nanosegundos antes de escribir los puntos de datos.

    La función create_bucket crea un nuevo bucket en la base de datos de destino con una duración infinita.

    Finalmente, la función query_oss realiza una consulta a la base de datos de origen y muestra los resultados.


## python_realtime.py

    Este código en Python es un programa principal que recoge datos en tiempo real del coche y los almacena en una base de datos InfluxDB.

    Primero, el código importa varias bibliotecas y módulos necesarios, incluyendo InfluxDBClient para interactuar con la base de datos InfluxDB, keyboard para detectar las pulsaciones de teclas, y varios módulos personalizados como functions_reader, functions_utils y config.

    Luego, el código establece una conexión con la base de datos InfluxDB utilizando las credenciales y la URL proporcionadas en el módulo config.

    El programa entra en un bucle que se ejecuta hasta que la variable END se establece en True. Dentro de este bucle:

        1. Solicita al usuario que introduzca el nombre de un piloto y un circuito utilizando la función rundata().
        2. Crea un nuevo bucket en la base de datos InfluxDB con la función createbucket(), utilizando el nombre del piloto y del circuito como parte del nombre del bucket.
        3. Recibe datos del coche de carreras con la función rxnrf24() y los almacena en la base de datos InfluxDB.
