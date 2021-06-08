"""
Created on Fri Apr 10 04:52:17 2020

@author: and1
"""

import numpy as np
import matplotlib.pyplot as plt

import TCC_elements

n_of_steps = 4

bm1 = TCC_elements.Beam(base=0.25*25.4, height=0.5*25.4, length=250)
sh1 = TCC_elements.Shaft(diameter=0.5*25.4, length=120)
sg1 = TCC_elements.WheatstoneBridgeQuarter(circuit_voltage=5, gauge_factor=3)
amp1 = TCC_elements.SignalAmplifier(amp_factor=128)

# arrays for load cases
beam_load = np.linspace(100,1000,n_of_steps)
shaft_torque = np.linspace(1000,10000,n_of_steps)  # 1Nm to 10Nm

# output_voltages
V_out_sg_beam = sg1.output_voltage(bm1.deformation_for_load(load = beam_load))
V_out_sg_shaft = sg1.output_voltage(sh1.deformation_for_torque(torque = shaft_torque))

# amplified sg output voltages
V_out_sg_beam_amped = amp1.signal_amplification(V_out_sg_beam)
V_out_sg_shaft_amped = amp1.signal_amplification(V_out_sg_shaft)

# plot
plt.figure()
plt.title("Strain gauge output voltage on cantilever beam")
plt.xlabel("load [N]")
plt.ylabel("voltage [V]")
plt.plot(beam_load, V_out_sg_beam_amped, 'r')
plt.figure()
plt.title("Strain gauge output voltage on shaft")
plt.xlabel("torque [Nm]")
plt.ylabel("voltage [V]")
plt.plot(shaft_torque/1E3, V_out_sg_shaft_amped, 'b')
plt.show()
