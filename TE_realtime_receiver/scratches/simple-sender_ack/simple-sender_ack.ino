//Este codigo esta hecho para ir con simple-receiver.py
//Arduino nano con modulo nrf24l01 y el python en una rpi 4.
//Asegurar que los pines estan bien conectados y definidos en el codigo.


// DHT sensor library, version 1.4.0 by Adafruit
//#include <DHT.h>

// RF24, version 1.3.9, by TMRh20
#include <printf.h>
#include <RF24.h>

//#define PIN_DHT                  2            // PIN for DHT sensor communication.

#define PIN_RF24_CSN             10            // CSN PIN for RF24 module.
#define PIN_RF24_CE             9            // CE PIN for RF24 module.

#define NRF24_CHANNEL          100            // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_DYNAMIC_PAYLOAD    1
#define NRF24_PAYLOAD_SIZE      32            // Max. 32 bytes.
#define NRF24_PA_LEVEL           RF24_PA_MIN  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
#define NRF24_RETRY_DELAY        5            // Delay bewteen retries, 1..15.  Multiples of 250µs.
#define NRF24_RETRY_COUNT       15            // Number of retries, 1..15.

#define PROTOCOL 0x01                         // 0x01 (byte), temperature (float), humidity (float)
                                              // Python 1: "<Bff"

//#define DHT_TYPE              DHT22           // Type of DHT sensor:
                                              // DHT11, DHT12, DHT21, DHT22 (AM2302), AM2301

// Cretate NRF24L01 radio.
RF24 radio(PIN_RF24_CE, PIN_RF24_CSN);

// Create DHT sensor
//DHT dht(PIN_DHT, DHT_TYPE);

byte rf24_tx[6] = "1SNSR";    // Address used when transmitting data.
byte payload[32];             // Payload bytes. Used both for transmitting and receiving

unsigned long last_reading;                // Milliseconds since last measurement was read.
unsigned long ms_between_reads = 500;    // 10000 ms = 10 seconds


// Variables for sine and cosine waves
float time = 0.0;
float time_step = 0.1; // Adjust this value to change the frequency of the sine and cosine waves

void setup() {

  // Initialize serial connection.
  Serial.begin(9600);
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
    // Calculate sine and cosine values
    float sin_val = sin(radians(time));
    float cos_val = cos(radians(time));

    // Print sine and cosine values
    Serial.print("Sensor values: sin="); Serial.print(sin_val);
    Serial.print(", cos="); Serial.println(cos_val);

    // Stop listening on the radio (we can't both listen and send).
    radio.stopListening();

    // Send the data ...
    send_reading(PROTOCOL, sin_val, cos_val);

    // Start listening again.
    radio.startListening();

    // Wait for ACK payload.
    if (radio.available()) {
        byte ackPayload[NRF24_PAYLOAD_SIZE];
        radio.read(ackPayload, sizeof(ackPayload));
        int functionNumber = ackPayload[0];  // Assuming the function number is in the first byte of the ACK payload.
        executeFunction(functionNumber);


    // Register that we have read the temperature and humidity.
    last_reading = millis();

    // Increment time
    time += time_step;
  }
}

void executeFunction(int functionNumber) {
  switch (functionNumber) {
    case 1:
      // Execute function 1.
      break;
    case 2:
      // Execute function 2.
      break;
    // ... (resto de los casos) ...
    default:
      // Unknown function number.
      break;
  }
}

void send_reading(byte protocol, float temperature, float humidity)
{
  Serial.print("Bytes packed: ");
  Serial.println(sizeof(payload));
  int offset = 0;
  Serial.println("Preparing payload.");
  memcpy(payload + offset, (byte *)(&protocol), sizeof(protocol)); offset += sizeof(protocol);
  memcpy(payload + offset, (byte *)(&temperature), sizeof(temperature)); offset += sizeof(temperature);
  memcpy(payload + offset, (byte *)(&humidity), sizeof(humidity)); offset += sizeof(humidity);
  Serial.print("Bytes packed: "); Serial.println(offset);

  if (radio.write(payload, offset)) {
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
  
  //radio.setAutoAck(true);
  radio.enableAckPayload();

  radio.setPALevel(NRF24_PA_LEVEL);
  radio.setRetries(NRF24_RETRY_DELAY, NRF24_RETRY_COUNT);
  radio.setDataRate(NRF24_DATA_RATE);
  radio.setChannel(NRF24_CHANNEL);
  radio.setCRCLength(NRF24_CRC_LENGTH);
  radio.setPayloadSize(NRF24_PAYLOAD_SIZE);
  radio.openWritingPipe(rf24_tx);
  radio.stopListening();
}
