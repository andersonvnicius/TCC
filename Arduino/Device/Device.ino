
#include "Wire.h"
#include "Adafruit_ADS1X15.h"

Adafruit_ADS1115 ads;

int delay_time = 25;

void setup() {
  Serial.begin(115200);

  ads.setGain(GAIN_SIXTEEN);    // 16x  +/- 0.256V  1 bit = 0.0078125mV
  ads.begin();
}


void loop() {
  int16_t ads_value = ads.readADC_Differential_0_1();
  Serial.println(ads_value);
  delay(delay_time);
}
