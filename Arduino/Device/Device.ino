/*
Script TCC
*/

#include "Wire.h"
#include "MPU9250.h"
#include "Adafruit_ADS1X15.h"


//#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
//#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
//#endif


MPU9250 IMU(Wire,0x68);
Adafruit_ADS1115 ads;


int delay_time = 100;

void setup() {
  Serial.begin(115200);
  
  int status;
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  
  // ADC Gain control, never exceed the upper and lower limits if you adjust the input range, otherwise these values may destroy your ADC!
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x +/- 6.144V  1 bit = 0.1875mV
  // ads.setGain(GAIN_ONE);        // 1x   +/- 4.096V  1 bit = 0.125mV
  // ads.setGain(GAIN_TWO);        // 2x   +/- 2.048V  1 bit = 0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x   +/- 1.024V  1 bit = 0.03125mV
  ads.setGain(GAIN_EIGHT);      // 8x   +/- 0.512V  1 bit = 0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x  +/- 0.256V  1 bit = 0.0078125mV
  
  ads.begin();
}


void loop() {
  IMU.readSensor();  // IMU
  float accel_x = IMU.getAccelX_mss();
  float accel_y = IMU.getAccelY_mss();
  float accel_z = IMU.getAccelZ_mss();
  float giro_x = IMU.getGyroX_rads();
  float giro_y = IMU.getGyroX_rads();
  float giro_z = IMU.getGyroZ_rads();
  int16_t ads_value = ads.readADC_Differential_0_1();
  Serial.print(accel_x); Serial.print(" ");
  Serial.print(accel_y); Serial.print(" ");
  Serial.print(accel_z); Serial.print(" ");
  Serial.print(giro_x); Serial.print(" ");
  Serial.print(giro_y); Serial.print(" ");
  Serial.print(giro_z); Serial.print(" ");
  Serial.println(ads_value);
  delay(delay_time);
}
