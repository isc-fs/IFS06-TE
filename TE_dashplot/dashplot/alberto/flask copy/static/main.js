//Conection con el flask server. (En el navegador hay que abrir esta dirección)
var socket = io.connect('http://127.0.0.1:5000')


// El delay repreenta que los puntos estarán fuera del gráfico 2 segundos después de que se hayan recibido. (Se mueve hacia la izquierda vamos)
var ctx1 = document.getElementById('myChart_pedals').getContext('2d');
var chart1 = new Chart(ctx1, {
    type: 'line',
    data: {
        datasets: [{
            label: 'throttle',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'brake',
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

var ctx2 = document.getElementById('myChart_TEMP_FRENOS').getContext('2d');
var chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'TFR',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'TFL',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }, {
            label: 'TRR',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false
        }, {
            label: 'TRL',
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

// myChart_IMU REAR ax ay az
var ctx9 = document.getElementById('myChart_IMU_REAR').getContext('2d');
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

// myChart_IMU REAR GyroX GyroY GyroZ
var ctx10 = document.getElementById('myChart_IMU_REAR_2').getContext('2d');
var chart10 = new Chart(ctx10, {
    type: 'line',
    data: {
        datasets: [{
            label: 'GyroX',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'GyroY',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }, {
            label: 'GyroZ',
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


var ctx11 = document.getElementById('myChart_GPS_Speed').getContext('2d');
var chart11 = new Chart(ctx11, {
    type: 'line',
    data: {
        datasets: [{
            label: 'speed',
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
// Ver si se puede hacer otro tipo de gráfico para GPS
var ctx12 = document.getElementById('myChart_GPS').getContext('2d');
var chart12 = new Chart(ctx12, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Latitude',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'Longitude',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        },{
            label: 'Altitude',
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

var ctx14 = document.getElementById('myChart_cell').getContext('2d');
var chart14 = new Chart(ctx14, {
    type: 'line',
    data: {
        datasets: [{
            label: 'cell_min_v',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }, {
            label: 'cell_max_temp',
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

var ctx15 = document.getElementById('myChart_current').getContext('2d');
var chart15 = new Chart(ctx15, {
    type: 'line',
    data: {
        datasets: [{
            label: 'current_sensor',
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
var ctx16 = document.getElementById('myChart_inverter_in').getContext('2d');
var chart16 = new Chart(ctx16, {
    type: 'line',
    data: {
        datasets: [{
            label: 'inverter_in',
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
var ctx17 = document.getElementById('myChart_inverter_out').getContext('2d');
var chart17 = new Chart(ctx17, {
    type: 'line',
    data: {
        datasets: [{
            label: 'inverter_out',
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
var ctx18 = document.getElementById('myChart_motor_in').getContext('2d');
var chart18 = new Chart(ctx18, {
    type: 'line',
    data: {
        datasets: [{
            label: 'motor_in',
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
var ctx19 = document.getElementById('myChart_motor_out').getContext('2d');
var chart19 = new Chart(ctx19, {
    type: 'line',
    data: {
        datasets: [{
            label: 'motor_out',
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


socket.on('newdata', function(data) {
    if (data.dataid == 0x610) { // IMU REAR
        if (chart9.data.datasets[0] && chart9.data.datasets[1] && chart9.data.datasets[2]) {
            chart9.data.datasets[0].data.push({x: Date.now(), y: data.ax});
            chart9.data.datasets[1].data.push({x: Date.now(), y: data.ay});
            chart9.data.datasets[2].data.push({x: Date.now(), y: data.az});
            chart9.update();
        }
        if (chart10.data.datasets[0] && chart10.data.datasets[1] && chart10.data.datasets[2]) {
            chart10.data.datasets[0].data.push({x: Date.now(), y: data.GyroX});
            chart10.data.datasets[1].data.push({x: Date.now(), y: data.GyroY});
            chart10.data.datasets[2].data.push({x: Date.now(), y: data.GyroZ});
            chart10.update();
        }
    } else if (data.dataid == 0x600) { // MOTOR INVERSOR
        if (chart3.data.datasets[0]) {
            chart3.data.datasets[0].data.push({x: Date.now(), y: data.dc_bus_voltage});
            chart3.update();
        }
        if (chart4.data.datasets[0]) {
            chart4.data.datasets[0].data.push({x: Date.now(), y: data.i_actual});
            chart4.update();
        }
        if (chart5.data.datasets[0]) {
            chart5.data.datasets[0].data.push({x: Date.now(), y: data.igbt_temp});
            chart5.update();
        }
        if (chart6.data.datasets[0]) {
            chart6.data.datasets[0].data.push({x: Date.now(), y: data.inverter_temp});
            chart6.update();
        }
        if (chart7.data.datasets[0]) {
            chart7.data.datasets[0].data.push({x: Date.now(), y: data.motor_temp});
            chart7.update();
        }
        if (chart8.data.datasets[0]) {
            chart8.data.datasets[0].data.push({x: Date.now(), y: data.n_actual});
            chart8.update();
        }
    } else if (data.dataid == 0x630) { // PEDALS
        if (chart1.data.datasets[0] && chart1.data.datasets[1]) {
            chart1.data.datasets[0].data.push({x: Date.now(), y: data.throttle});
            chart1.data.datasets[1].data.push({x: Date.now(), y: data.brake});
            chart1.update();
        }
    } else if (data.dataid == 0x640) { // ACCUMULADOR
        if (chart14.data.datasets[0] && chart14.data.datasets[1]) {
            chart14.data.datasets[0].data.push({x: Date.now(), y: data.cell_min_v});
            chart14.data.datasets[1].data.push({x: Date.now(), y: data.cell_max_temp});
            chart14.update();
        }
        if (chart15.data.datasets[0]) {
            chart15.data.datasets[0].data.push({x: Date.now(), y: data.current_sensor});
            chart15.update();
        }
    } else if (data.dataid == 0x650) { // GPS
        if (chart11.data.datasets[0]) {
            chart11.data.datasets[0].data.push({x: Date.now(), y: data.speed});
            chart11.update();
        }
        if (chart12.data.datasets[0] && chart12.data.datasets[1] && chart12.data.datasets[2]) {
            chart12.data.datasets[0].data.push({x: Date.now(), y: data.lat});
            chart12.data.datasets[1].data.push({x: Date.now(), y: data.long});
            chart12.data.datasets[2].data.push({x: Date.now(), y: data.alt});
            chart12.update();
        }
    } else if (data.dataid == 0x670) { // SUSPENSION
        if (chart13.data.datasets[0] && chart13.data.datasets[1] && chart13.data.datasets[2] && chart13.data.datasets[3]) {
            chart13.data.datasets[0].data.push({x: Date.now(), y: data.FR});
            chart13.data.datasets[1].data.push({x: Date.now(), y: data.FL});
            chart13.data.datasets[2].data.push({x: Date.now(), y: data.RR});
            chart13.data.datasets[3].data.push({x: Date.now(), y: data.RL});
            chart13.update();
        }
    } else if (data.dataid == 0x660) { // INVERTER & MOTOR
        if (chart16.data.datasets[0]) {
            chart16.data.datasets[0].data.push({x: Date.now(), y: data.inverter_in});
            chart16.update();
        }
        if (chart17.data.datasets[0]) {
            chart17.data.datasets[0].data.push({x: Date.now(), y: data.inverter_out});
            chart17.update();
        }
        if (chart18.data.datasets[0]) {
            chart18.data.datasets[0].data.push({x: Date.now(), y: data.motor_in});
            chart18.update();
        }
        if (chart19.data.datasets[0]) {
            chart19.data.datasets[0].data.push({x: Date.now(), y: data.motor_out});
            chart19.update();
        }
    } else if (data.dataid == 0x680) { // TEMP FRENOS
        if (chart2.data.datasets[0] && chart2.data.datasets[1] && chart2.data.datasets[2] && chart2.data.datasets[3]) {
            chart2.data.datasets[0].data.push({x: Date.now(), y: data.TFR});
            chart2.data.datasets[1].data.push({x: Date.now(), y: data.TFL});
            chart2.data.datasets[2].data.push({x: Date.now(), y: data.TRR});
            chart2.data.datasets[3].data.push({x: Date.now(), y: data.TRL});
            chart2.update();
        }
    }
});
