def writerundata(bucketnever,bucket,piloto,circuito):
    '''
    Esta función escribe datos en dos buckets de InfluxDB. 
    Los datos son puntos que representan información sobre un piloto y un circuito. 
    Los puntos se escriben en ambos buckets proporcionados como argumentos.
    '''
    write_api = client.write_api(write_options=SYNCHRONOUS)


    p = Point("piloto").field("data",piloto)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)


    p = Point("circuito").field("data",circuito)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)


def rundata():
    '''
     Esta función solicita al usuario que introduzca el nombre de un piloto y un circuito. 
     Devuelve estos dos valores.
    '''


    piloto = input("Introducir el nombre del piloto: ")
    circuito = input("Introducir el nombre del circuito: ")

    return piloto,circuito



def createbucket(piloto,circuito):
    '''
     Esta función crea dos nuevos buckets en una base de datos InfluxDB. 
     Los nombres de los buckets se generan dinámicamente basándose en la hora actual y 
     en la información del piloto y del circuito proporcionados. 
     La función devuelve el ID del bucket creado.
    '''
    headers = {'Authorization': f'Token {token}'}
    url = "http://localhost:8086/api/v2/buckets"
    payloadtemp = {
    "orgID": org,
    "name": "ISC",
    "description": "create a bucket",
    "rp": "myrp",
    "retentionRules":[
    {
    "type": "expire",
    "everySeconds": 86400
    }
    ]
    }

    test = datetime.now()
    time = test.strftime("%Y-%m-%d %H:%M:%S")
    print(time)

    payloadnever = {
    "orgID": org,
    "name": time+" |> FS-"+circuito+"-"+piloto,
    "description": "create a bucket",
    "rp": "myrp",
    "duration":"INF"
    }

    # "type": "expire","everySeconds": 86400 // es 1 dia
    #Para crear un rp que no se borre quitas retentionRules y pones "duration": "INF"
    #No se puede crear un bucket con el mismo nombre que uno ya existente

    r1 = requests.post(url, headers=headers, json=payloadnever)
    r2 = requests.post(url, headers=headers, json=payloadtemp)
    #print(r.text.split(",")[0].split(":")[1].replace('"',"").replace(" ",""))
    #print(r.text)
    return r1.text.split(",")[0].split(":")[1].replace('"',"").replace(" ","")
    #r.text.split(",")[0].split(":")[1].replace('"',"").replace(" ","") de aqui sacas el id del bucket creado
