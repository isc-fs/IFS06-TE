#include <SPI.h>
// #include <nRF24L01.h>
#include <RF24.h>
#include <printf.h>
#define PIN_DHT                  2            // PIN for DHT sensor communication.

#define PIN_RF24_CSN             10            // CSN PIN for RF24 module.
#define PIN_RF24_CE             9          // CE PIN for RF24 module.

#define NRF24_CHANNEL          100            // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_DYNAMIC_PAYLOAD    1
#define NRF24_PAYLOAD_SIZE      32            // Max. 32 bytes. Hay que ver cuanto se incrementa, actulizar recepción
#define NRF24_PA_LEVEL           RF24_PA_MIN  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
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
unsigned long ms_between_reads = 100;    // 10000 ms = 10 seconds

void setup() {
  //Inicializar el número aleatorio
  randomSeed(analogRead(0));

  // Initialize serial connection.
  Serial.begin(9600);//@TODO: ver si bajar la velocidad de transmisión
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
    // Generate random dataid
    float dataids[] = {0x600, 0x610, 0x630, 0x640, 0x650, 0x660, 0x670, 0x680};
    float dataid = dataids[random(8)];
    sendData(dataid);
    last_reading = millis();
  }
}

void sendData(int dataid) {
  float values[7];
  for (int i = 0; i < 6; i++) {
    values[i] = random(100) / 1.0;
  }

  Serial.print("DataID: "); Serial.println(dataid, HEX);
  Serial.print("Values: ");
  for (int i = 0; i < 7; i++) {
    Serial.print(values[i]); Serial.print(" ");
  }
  Serial.println();

  int offset = 0;
  memset(payload, 0, sizeof(payload));

  byte dataid_bytes[sizeof(dataid)];
  memcpy(dataid_bytes, &dataid, sizeof(dataid));
  memcpy(payload + offset, dataid_bytes, sizeof(dataid_bytes));
  offset += sizeof(dataid_bytes);

  //memcpy(payload + offset, (byte *)(&dataid), sizeof(dataid)); 
  offset += sizeof(dataid);
  switch (dataid) {
    case 0x600: // MOTOR INVERSOR
      memcpy(payload + offset, values, sizeof(float) * 6); 
      offset += sizeof(float) * 6;
      break;
    case 0x610: // IMU REAR
      memcpy(payload + offset, values, sizeof(float) * 6); 
      offset += sizeof(float) * 6;
      break;
    case 0x630: // PEDALS
      memcpy(payload + offset, values, sizeof(float) * 2); 
      offset += sizeof(float) * 2;
      break;
    case 0x640: // ACUMULADOR
      memcpy(payload + offset, values, sizeof(float) * 3); 
      offset += sizeof(float) * 3;
      break;
    case 0x650: // GPS
      memcpy(payload + offset, values, sizeof(float) * 4); 
      offset += sizeof(float) * 4;
      break;
    case 0x660: // INVERTER & MOTOR
      memcpy(payload + offset, values, sizeof(float) * 4); 
      offset += sizeof(float) * 4;
      break;
    case 0x670: // SUSPENSION
      memcpy(payload + offset, values, sizeof(float) * 4); 
      offset += sizeof(float) * 4;
      break;
    case 0x680: // TEMP Frenos
      memcpy(payload + offset, values, sizeof(float) * 4);
      offset += sizeof(float) * 4;
      break;
    default:
      memcpy(payload + offset, values, sizeof(float)); 
      offset += sizeof(float);
      break;
  }

  // Ensure the payload is 32 bytes
  while (offset < 32) {
    payload[offset] = 0;
    offset++;
    }
  Serial.print("Payload: ");
  for (int i = 0; i < 8; i++) {
    Serial.print(payload[i]); Serial.print(" ");
  }
  Serial.println();


  if (radio.write(payload, offset)) {
    Serial.println("Payload sent successfully");
  } else {
    Serial.println("Failed to send payload");
  }
  //Serial.print(payload);
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
