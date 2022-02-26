/*
Script wifi datalogger
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Q2HX711.h>

#ifndef STASSID
#define STASSID "Unifique(Valentine)"
#define STAPSK  "valentops1812"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const byte hx711_data_pin = D2;
const byte hx711_clock_pin = D1;

Q2HX711 hx711(hx711_data_pin, hx711_clock_pin);

ESP8266WebServer server(80);

void handleRead() {
  if (server.method() != HTTP_POST) {
    server.send(405, "text/plain", "Method now allowed");
  } else {
    server.send(200, "text/plain", String(hx711.read()) + server.arg("plain"));
  }
}

void setup(void) {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/read", handleRead);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}