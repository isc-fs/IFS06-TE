// DHT sensor library, version 1.4.0 by Adafruit
#include <DHT.h>

// RF24, version 1.3.9, by TMRh20
#include <printf.h>
#include <RF24.h>

#define PIN_DHT                  2            // PIN for DHT sensor communication.

#define PIN_RF24_CSN             10            // CSN PIN for RF24 module.
#define PIN_RF24_CE             9          // CE PIN for RF24 module.

#define NRF24_CHANNEL          100            // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_DYNAMIC_PAYLOAD    1
#define NRF24_PAYLOAD_SIZE      77            // Max. 32 bytes. Hay que ver cuanto se incrementa, actulizar recepción
#define NRF24_PA_LEVEL           RF24_PA_MAX  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
#define NRF24_RETRY_DELAY        5            // Delay bewteen retries, 1..15.  Multiples of 250µs.
#define NRF24_RETRY_COUNT       15            // Number of retries, 1..15.

#define PROTOCOL 0x01                         // 0x01 (byte), temperature (float), humidity (float)
                                              // Python 1: "<Bff"

#define DHT_TYPE              DHT22           // Type of DHT sensor:
                                              // DHT11, DHT12, DHT21, DHT22 (AM2302), AM2301

// Cretate NRF24L01 radio.
RF24 radio(PIN_RF24_CE, PIN_RF24_CSN);

// Create DHT sensor
// DHT dht(PIN_DHT, DHT_TYPE);

byte rf24_tx[6] = "1SNSR";    // Address used when transmitting data.
byte payload[NRF24_PAYLOAD_SIZE];             // Payload bytes. Used both for transmitting and receiving

unsigned long last_reading = 0;                // Milliseconds since last measurement was read.
unsigned long ms_between_reads = 1000;    // 10000 ms = 10 seconds

void setup() 
{

  //Inicializar el número aleatorio
  randomSeed(analogRead(0));

  // Initialize serial connection.
  Serial.begin(9600); //@TODO: ver si bajar la velocidad de transmisión
  printf_begin();
  delay(100);

  // Show that program is starting.
  Serial.println("\n\nNRF24L01 Arduino Simple Sender.");

  // Configure the NRF24 tranceiver.
  Serial.println("Configure NRF24 ...");
  nrf24_setup();

  // Show debug information for NRF24 tranceiver.
  radio.printDetails();

  // Initialise the DHT sensor.
  //dht.begin();

  // Take the current timestamp. This means that the next (first) measurement will be read and
  // transmitted in "ms_between_reads" milliseconds.
  last_reading = 0;
  
}

void loop() {

  if (millis() - last_reading > ms_between_reads) {
    // Read sensor values every "ms_between_read" milliseconds.
    float temperature, humidity, pressure, dc_bus_voltage, i_actual, igbt_temp, inverter_temp, motor_temp, n_actual, ax, ay, az, brake, throttle, current_sensor, suspension_FR, suspension_FL, suspension_RR, suspension_RL;
    // Read the humidity and temperature.
    
    temperature = random(6);
    humidity = 50; 
    pressure = random(6); 
    dc_bus_voltage = random(6); 
    i_actual = random(6); 
    igbt_temp = random(6); 
    inverter_temp = random(6); 
    motor_temp = random(6); 
    n_actual = random(6); 
    ax = random(6); 
    ay = random(6); 
    az = random(6); 
    brake = random(6);
    throttle = random(6); 
    current_sensor = random(6); 
    suspension_FR = random(6); 
    suspension_FL = random(6); 
    suspension_RR = random(6);
    suspension_RL = random(6);

    

    Serial.println("Sensor values:");
    Serial.print("temperature=");Serial.print(temperature);
    Serial.print(", humidity="); Serial.print(humidity);
    Serial.print(", pressure="); Serial.print(pressure);
    Serial.print(", dc_bus_voltage="); Serial.print(dc_bus_voltage);
    Serial.print(", i_actual="); Serial.print(i_actual);
    Serial.print(", igbt_temp="); Serial.print(igbt_temp);
    Serial.print(", inverter_temp="); Serial.print(inverter_temp);
    Serial.print(", motor_temp="); Serial.print(motor_temp);
    Serial.print(", n_actual="); Serial.print(n_actual);
    Serial.print(", ax="); Serial.print(ax);
    Serial.print(", ay="); Serial.print(ay);
    Serial.print(", az="); Serial.print(az);
    Serial.print(", brake="); Serial.print(brake);
    Serial.print(", throttle="); Serial.print(throttle);
    Serial.print(", current_sensor="); Serial.print(current_sensor);
    Serial.print(", suspension_FR="); Serial.print(suspension_FR);
    Serial.print(", suspension_FL="); Serial.print(suspension_FL);
    Serial.print(", suspension_RR="); Serial.print(suspension_RR);
    Serial.print(", suspension_RL="); Serial.println(suspension_RL);



    // Stop listening on the radio (we can't both listen and send).
    radio.stopListening();

    // Send the data ...
    send_reading(PROTOCOL, temperature, humidity, pressure, dc_bus_voltage, i_actual, igbt_temp, inverter_temp, motor_temp, n_actual, ax, ay, az, brake, throttle, current_sensor, suspension_FR, suspension_FL, suspension_RR, suspension_RL);

    // Start listening again.
    radio.startListening();

    // Register that we have read the temperature and humidity.
    last_reading = millis();
  }
}

void send_reading(byte protocol, float temperature, float humidity, float  pressure, float  dc_bus_voltage, float  i_actual, float igbt_temp, float  inverter_temp, float  motor_temp, float  n_actual, float  ax, float  ay, float  az, float  brake, float throttle,  float current_sensor,  float suspension_FR,  float suspension_FL,  float suspension_RR, float suspension_RL)
{

  //Serial.print("Bytes packed(payload): ");
  //Serial.println(sizeof(payload));

  int offset = 0;
  Serial.println("Preparing payload...");
  memcpy(payload + offset, (byte *)(&protocol), sizeof(protocol)); offset += sizeof(protocol);
  memcpy(payload + offset, (byte *)(&temperature), sizeof(temperature)); offset += sizeof(temperature);
  memcpy(payload + offset, (byte *)(&humidity), sizeof(humidity)); offset += sizeof(humidity);
  memcpy(payload + offset, (byte *)(&pressure), sizeof(pressure)); offset += sizeof(pressure);
  memcpy(payload + offset, (byte *)(&dc_bus_voltage), sizeof(dc_bus_voltage)); offset += sizeof(dc_bus_voltage);
  memcpy(payload + offset, (byte *)(&i_actual), sizeof(i_actual)); offset += sizeof(i_actual);
  memcpy(payload + offset, (byte *)(&igbt_temp), sizeof(igbt_temp)); offset += sizeof(igbt_temp);
  memcpy(payload + offset, (byte *)(&inverter_temp), sizeof(inverter_temp)); offset += sizeof(inverter_temp);
  memcpy(payload + offset, (byte *)(&motor_temp), sizeof(motor_temp)); offset += sizeof(motor_temp);
  memcpy(payload + offset, (byte *)(&n_actual), sizeof(n_actual)); offset += sizeof(n_actual);
  memcpy(payload + offset, (byte *)(&ax), sizeof(ax)); offset += sizeof(ax);
  memcpy(payload + offset, (byte *)(&ay), sizeof(ay)); offset += sizeof(ay);
  memcpy(payload + offset, (byte *)(&az), sizeof(az)); offset += sizeof(az);
  memcpy(payload + offset, (byte *)(&brake), sizeof(brake)); offset += sizeof(brake);
  memcpy(payload + offset, (byte *)(&throttle), sizeof(throttle)); offset += sizeof(throttle);
  memcpy(payload + offset, (byte *)(&current_sensor), sizeof(current_sensor)); offset += sizeof(current_sensor);
  memcpy(payload + offset, (byte *)(&suspension_FR), sizeof(suspension_FR)); offset += sizeof(suspension_FR);
  memcpy(payload + offset, (byte *)(&suspension_FL), sizeof(suspension_FL)); offset += sizeof(suspension_FL);
  memcpy(payload + offset, (byte *)(&suspension_RR), sizeof(suspension_RR)); offset += sizeof(suspension_RR);
  memcpy(payload + offset, (byte *)(&suspension_RL), sizeof(suspension_RL)); offset += sizeof(suspension_RL);
  Serial.print("Bytes packed: "); Serial.println(offset);

  if (radio.write(payload, offset)) {
    // Añadir aquí lo del ack
    Serial.print("Payload sent successfully. Retries="); Serial.println(radio.getARC());
  }
  else {
    Serial.print("Failed to send payload. Retries="); Serial.println(radio.getARC());
  }
}

void nrf24_setup()
{
  radio.begin();
  radio.enableDynamicPayloads();
  radio.setAutoAck(true);
  radio.setPALevel(NRF24_PA_LEVEL);
  radio.setRetries(NRF24_RETRY_DELAY, NRF24_RETRY_COUNT);
  radio.setDataRate(NRF24_DATA_RATE);
  radio.setChannel(NRF24_CHANNEL);
  radio.setCRCLength(NRF24_CRC_LENGTH);
  radio.setPayloadSize(NRF24_PAYLOAD_SIZE);
  radio.openWritingPipe(rf24_tx);
  radio.stopListening();
}
