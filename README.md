# Low cost dynamic torque sensor

## What it is

It is a sensor to live-monitor the torsional loads on a shaft caused by engines, gearboxes, tyre longitudinal forces, etc.

### How it works

It uses an sensor called strain gauge, this tyoe of sensor is glued to a component's surface and when this surface is under a mechanical load it will deform, since the strain gauge is totally glued to the surface this deformation will also happen in the strain gauge surface, when this happens there will be a change in the sensor's electrical resistance, if a voltage is applied in a system of strain gauges you can use an Arduino controller to read this difference of resistance, which using some basic math and calibration can be converted to a pretty accurate load value.

### Technology

The technologies i'm using to develop the system at this time is listed below:

An ESP32 controller board to control the system, and read the signals sent by the signal amplifier ADS1115, it needs to be used beacuse the defference in voltage caused by the strain gauge deformation is too low for the controller to accurately read, an 6 axis acelerometer because I want to know at which angular speed the shaft that the device is attached to it is reving (which I can use to extract the power values in HP or kW), and a wheatstone brigde circuit comprised of four strain gauges which I use for reading the torsional loads themseves.

I'm still evaluating which communication protocol is the best alternative for live-data gathering in my case, one the main advantages of the ESP32 controller is that it has built in Bluetooth low energy and wifi transmitters and receivers.

## How does it compare with high accuracy sistems

That's the main focus of my thesys, and when I run the experiments I will have an answer to this question in particular, if the accuracy is good enough I pretend to implement this system in college competition vehicles (Baja SAE, Formula SAE, etc) for live-telemetry and data gathering.
