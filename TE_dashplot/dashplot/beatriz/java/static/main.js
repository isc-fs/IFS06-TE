//Conection con el flask server. (En el navegador hay que abrir esta dirección)
var socket = io.connect('http://127.0.0.1:5000')

//Habría que investigar más sobre chart.js que esto me lo han hecho jajajaj
// El delay repreenta que los puntos estarán fuera del gráfico 2 segundos después de que se hayan recibido. (Se mueve hacia la izquierda vamos)
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Temperature',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'Humidity',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                type: 'realtime',
                realtime: {
                    delay: 2000
                }
            },
            y: {
                beginAtZero: true
            }
        }
    }
});

//Important!!: escucha el evento 'newdata' que se emite desde el servidor, cuando el servidor emite evento, esta función se llama con los datos obtenidos del servidor. 
//chart.data.datasets[0].data.push({x: Date.now(), y: data.temperature}); añade un nuevo punto al gráfico.
//char.update actualiza el gráfico con los datos recibidos.
//muy guay porque no se vuelve a crear todo el gráfico cada vez que se recibe un dato, sino que se actualiza el gráfico con los datos recibidos

socket.on('newdata', function(data) {
    chart.data.datasets[0].data.push({x: Date.now(), y: data.temperature});
    chart.data.datasets[1].data.push({x: Date.now(), y: data.humidity});
    chart.update();
});