"""
Created on Wed Apr  8 22:17:01 2020

Computational elements for simulations that will be used in the project

Default input units: mm, kg, seconds

@author: and1
"""


class Beam:
    def __init__(self, base, height, length, material="steel"):
        self.base = base  # mm
        self.height = height  # mm
        self.length = length  # mm
        self.material = material

        if self.material == "steel":
            self.E = 210E3  # N/mm**2

    def deformation_for_load(self, load, position="end"):
        if position == 'end':
            position = self.length
        elif position > self.length:
            return "invalid load position"
        return 6 * load * position / (self.E * self.base * self.height ** 2)


class Shaft:
    def __init__(self, diameter, length, material="steel"):
        self.diameter = diameter
        self.length = length
        self.material = material

        if self.material == "steel":
            self.G = 69.3E3  # N/mm**2

    def deformation_for_torque(self, torque):  # N*mm
        from numpy import pi
        return 32 * torque * self.length / (pi * self.G * self.diameter ** 4)


class WheatstoneBridgeQuarter:
    def __init__(self, circuit_voltage, gauge_factor):
        self.circuit_voltage = circuit_voltage
        self.gauge_factor = gauge_factor

    def output_voltage(self, deflection):
        return self.circuit_voltage * ((self.gauge_factor * deflection) / (4 + self.gauge_factor * deflection))


class SignalAmplifier:
    def __init__(self, amp_factor):
        self.amp_factor = amp_factor

    def signal_amplification(self, input_voltage):
        """simular o diagrama de bode do amp de sinal (??)"""
        return self.amp_factor * input_voltage
