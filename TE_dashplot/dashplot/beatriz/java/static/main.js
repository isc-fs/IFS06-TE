//Conection con el flask server. (En el navegador hay que abrir esta dirección)
var socket = io.connect('http://127.0.0.1:5000')

//Habría que investigar más sobre chart.js que esto me lo han hecho jajajaj
// El delay repreenta que los puntos estarán fuera del gráfico 2 segundos después de que se hayan recibido. (Se mueve hacia la izquierda vamos)
var ctx1 = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx1, {
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

var ctx2 = document.getElementById('myChart_P').getContext('2d');
var chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Pressure',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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

var ctx3 = document.getElementById('myChart_dc_bus_voltage').getContext('2d');
var chart3= new Chart(ctx3, {
    type: 'line',
    data: {
        datasets: [{
            label: 'dc_bus_voltage',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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

var ctx4 = document.getElementById('myChart_i_actual').getContext('2d');
var chart4 = new Chart(ctx4, {
    type: 'line',
    data: {
        datasets: [{
            label: 'i_actual',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


var ctx5 = document.getElementById('myChart_igbt_temp').getContext('2d');
var chart5 = new Chart(ctx5, {
    type: 'line',
    data: {
        datasets: [{
            label: 'igbt_temp',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


var ctx6 = document.getElementById('myChart_inverter_temp').getContext('2d');
var chart6 = new Chart(ctx6, {
    type: 'line',
    data: {
        datasets: [{
            label: 'inverter_temp',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


var ctx7 = document.getElementById('myChart_motor_temp').getContext('2d');
var chart7 = new Chart(ctx7, {
    type: 'line',
    data: {
        datasets: [{
            label: 'motor_temp',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


var ctx8 = document.getElementById('myChart_n_actual').getContext('2d');
var chart8 = new Chart(ctx8, {
    type: 'line',
    data: {
        datasets: [{
            label: 'n_actual',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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

// myChart_a
var ctx9 = document.getElementById('myChart_a').getContext('2d');
var chart9 = new Chart(ctx9, {
    type: 'line',
    data: {
        datasets: [{
            label: 'ax',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'ay',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }, {
            label: 'az',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
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


var ctx10 = document.getElementById('myChart_brake').getContext('2d');
var chart10 = new Chart(ctx10, {
    type: 'line',
    data: {
        datasets: [{
            label: 'brake',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


var ctx11 = document.getElementById('myChart_throttle').getContext('2d');
var chart11 = new Chart(ctx11, {
    type: 'line',
    data: {
        datasets: [{
            label: 'throttle',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
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


// myChart_suspension will have 4 lines Suspension_FR, Suspension_FL, Suspension_RR, Suspension_RL
var ctx13 = document.getElementById('myChart_suspension').getContext('2d');

var chart13 = new Chart(ctx13, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Suspension_FR',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'Suspension_FL',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }, {
            label: 'Suspension_RR',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false
        }, {
            label: 'Suspension_RL',
            data: [],
            borderColor: 'rgba(255, 206, 86, 1)',
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

socket.on('newdata', function(data) {
    chart.data.datasets[0].data.push({x: Date.now(), y: data.temperature});
    chart.data.datasets[1].data.push({x: Date.now(), y: data.humidity});
    
    chart2.data.datasets[0].data.push({x: Date.now(), y: data.pressure});
    
    chart3.data.datasets[0].data.push({x: Date.now(), y: data.dc_bus_voltage});
    
    chart4.data.datasets[0].data.push({x: Date.now(), y: data.i_actual});
    
    chart5.data.datasets[0].data.push({x: Date.now(), y: data.igbt_temp});
    
    chart6.data.datasets[0].data.push({x: Date.now(), y: data.inverter_temp});
    
    chart7.data.datasets[0].data.push({x: Date.now(), y: data.motor_temp});
    
    chart8.data.datasets[0].data.push({x: Date.now(), y: data.n_actual});

    //este tiene 3 
    chart9.data.datasets[0].data.push({x: Date.now(), y: data.ax});
    chart9.data.datasets[1].data.push({x: Date.now(), y: data.ay});
    chart9.data.datasets[2].data.push({x: Date.now(), y: data.az});

    chart10.data.datasets[0].data.push({x: Date.now(), y: data.brake});
    
    chart11.data.datasets[0].data.push({x: Date.now(), y: data.throttle});

    //chart12.data.datasets[0].data.push({x: Date.now(), y: data.inverter_temp});

    //este tiene 4
    chart13.data.datasets[0].data.push({x: Date.now(), y: data.suspension_FR});
    chart13.data.datasets[1].data.push({x: Date.now(), y: data.suspension_FL});
    chart13.data.datasets[2].data.push({x: Date.now(), y: data.suspension_RR});
    chart13.data.datasets[3].data.push({x: Date.now(), y: data.suspension_RL});


    
    chart.update();
    chart2.update();
    chart3.update();
    chart4.update();
    chart5.update();
    chart6.update();
    chart7.update();
    chart8.update();
    chart9.update();
    chart10.update();
    chart11.update();
    chart13.update();

});