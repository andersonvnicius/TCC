"""
Description:
Thesis test bench simulation

Assume:
Shaft is only subjected to torque
"""


from numpy import pi, cos, sin, deg2rad
import numpy as np
import matplotlib.pyplot as plt


def polar_inertia_circular_section(diameter_ext, diameter_int=0.):
    return pi*(diameter_ext**4-diameter_int**4)/32


def shear_tension_on_shaft(torque_in, shaft_diameter_ext, shaft_diameter_int=0.):
    return torque_in*(shaft_diameter_ext/2)/(polar_inertia_circular_section(shaft_diameter_ext, shaft_diameter_int))


def deformation_on_plane(epsilon_x=0., epsilon_y=0., gamma_xy=0., theta=0.):
    epsilon_x_line = (epsilon_x + epsilon_y)/2 + ((epsilon_x - epsilon_y)/2)*cos(2*theta) + (gamma_xy/2)*sin(2*theta)
    epsilon_y_line = (epsilon_x + epsilon_y)/2 - ((epsilon_x - epsilon_y)/2)*cos(2*theta) - (gamma_xy/2)*sin(2*theta)
    gamma_xy_plane = 2*((-(epsilon_x - epsilon_y)/2)*sin(2*theta) + (gamma_xy/2)*cos(2*theta))
    return epsilon_x_line, epsilon_y_line, gamma_xy_plane


n_of_steps = 100

"""input_data"""
T = 1.1  # Nm
d_out = 3*25.4E-3/4  # m
d_in = d_out - 2.5e-3
G = 24E9  # GPa
plane_angle = deg2rad(45)
angles = np.linspace(0, 90, n_of_steps)

"""solution"""
tau = shear_tension_on_shaft(T, d_out, d_in)
shear_xy = tau/G
deform = deformation_on_plane(epsilon_x=0, epsilon_y=0, gamma_xy=shear_xy, theta=deg2rad(angles))

"""plots"""
"""
plt.figure()
plt.style.use('fivethirtyeight')
plt.plot(angles, deform[0]*1e5, 'b')
plt.plot(angles, deform[1]*1e5, 'g')
plt.plot(angles, deform[2]*1e5, 'r')
plt.xlabel('angle [deg]')
plt.ylabel('deformation [micrometer]')
plt.legend(['epsilon_x_line', 'epsilon_y_line', 'gamma_xy_plane'])
plt.show()
"""
