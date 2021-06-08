"""
test bench simulation
"""

from numpy import pi, cos, sin, deg2rad
import numpy as np
import matplotlib.pyplot as plt


def inertia_tube_section(diameter_ext, diameter_int):
    return pi*(diameter_ext**4 - diameter_int**4)/64


def polar_inertia_tube_section(diameter_ext, diameter_int):
    return pi*(diameter_ext**4 - diameter_int**4)/32


def first_moment_of_area_tube_section(diameter_ext, diameter_int):
    return 4*((diameter_ext/2)**3 - (diameter_int/2)**3)/6


def shear_stress_torsion(T, rho, J):
    return T*rho/J


def shear_stress_beam(V, Q, I, t):
    return V*Q/(I*t)


def deformation_on_plane(epsilon_x=0., epsilon_y=0., gamma_xy=0., theta=0.):
    epsilon_x_line = (epsilon_x + epsilon_y)/2 + ((epsilon_x - epsilon_y)/2)*cos(2*theta) + (gamma_xy/2)*sin(2*theta)
    epsilon_y_line = (epsilon_x + epsilon_y)/2 - ((epsilon_x - epsilon_y)/2)*cos(2*theta) - (gamma_xy/2)*sin(2*theta)
    gamma_xy_plane = 2*((-(epsilon_x - epsilon_y)/2)*sin(2*theta) + (gamma_xy/2)*cos(2*theta))
    return epsilon_x_line, epsilon_y_line, gamma_xy_plane


def strain_gauge_resistance_read(nominal_resistance, gauge_factor, strain):
    return nominal_resistance + gauge_factor*strain*nominal_resistance


def wheatstone_bridge_output(V_in, R1, R2, R3, R4):
    return V_in*(R4/(R1 + R4) - R3/(R2 + R3))


"""input data"""
load_applied = -10  # N
length_load_arm = 50E-3  # m  *torque applier tube length

length_tube = 70E-3  # m  *principal tube length
d_out = 3 * 25.4E-3 / 4  # m  *tube external diameter
d_in = d_out - 2.5e-3  # m
bearing_position = 50E-3  # m  *length to bearing

strain_gauge_angle = deg2rad(45)
strain_gauge_position = 20E-3  # m  *length to strain gauge
strain_gauge_gf = 2.2  # between 2 and 2.2
strain_gauge_nominal_resistance = 350  # ohms

circuit_voltage = 5  # V

# 6061-T6 material properties
E = 69E9  # GPa
G = 24E9  # GPa

"""solution"""

# section properties
I = inertia_tube_section(diameter_ext=d_out, diameter_int=d_in)
J = polar_inertia_tube_section(diameter_ext=d_out, diameter_int=d_in)
Q = first_moment_of_area_tube_section(diameter_ext=d_out, diameter_int=d_in)

# reactions and loads
reactions = np.linalg.solve(
    np.array([[0, -(bearing_position / length_tube)],
              [-1, -1]]),
    np.array([load_applied, load_applied])
)
torque_applied = load_applied * length_load_arm
shear_load = -reactions[1] - load_applied

# displacements
gamma_torque = shear_stress_torsion(T=torque_applied, rho=(d_out / 2), J=J)/G
gamma_beam_shear = shear_stress_beam(V=shear_load, Q=Q, I=I, t=(d_out - d_in))/G
gamma_xy = gamma_torque + gamma_beam_shear
displacements_sg = deformation_on_plane(epsilon_x=0, epsilon_y=0, gamma_xy=gamma_xy, theta=strain_gauge_angle)

# strain gauge readings
SG1 = SG3 = strain_gauge_resistance_read(strain_gauge_nominal_resistance, strain_gauge_gf, displacements_sg[0])
SG2 = SG4 = strain_gauge_resistance_read(strain_gauge_nominal_resistance, strain_gauge_gf, -displacements_sg[0])
bridge_reading = wheatstone_bridge_output(circuit_voltage, SG1, SG2, SG3, SG4)

# prints
print("")
print("general info")
print("load: ", load_applied, "N, ", " load_arm: ", length_load_arm*1e3, "mm ,", " torque: ", torque_applied, "Nm")
print("external tube diameter: ", round(d_out*1e3, 2), "mm ")
print("internal tube diameter: ", round(d_in*1e3 ,2), "mm")
print("resulting shear: ", gamma_xy)
print("")
print("displacements in main planes")
print("gamma torque: ", gamma_torque)
print("gamma beam shear:", gamma_beam_shear)
print("")
print("45degree strain gauge plane")
print("epsilon x' [mm]:", displacements_sg[0]*1e3)
print("epsilon y': [mm]", displacements_sg[1]*1e3)
print("gamma x'y':", displacements_sg[2])
print("")
print("bridge reading")
print("SG1 and SG3 reading", SG1)
print("SG2 and SG4 reading", SG2)
print("bridge output voltage", bridge_reading)
print("")

"""plots"""
n_of_steps = 15

# strain gauge angles analysis

angles = np.linspace(30, 60, n_of_steps)
deform = deformation_on_plane(epsilon_x=0, epsilon_y=0, gamma_xy=gamma_xy, theta=deg2rad(angles))

plt.figure(figsize=(10, 8))
plt.style.use('fivethirtyeight')
plt.plot(angles, deform[0] * 1e5, 'b')
plt.plot(angles, deform[1] * 1e5, 'g')
plt.plot(angles, deform[2] * 1e5, 'r')
plt.title('strain gauge deformation for different angles')
plt.xlabel('angle [deg]')
plt.ylabel('deformation [.01mm]')
plt.legend(['epsilon_x_line', 'epsilon_y_line', 'gamma_xy_plane'])
plt.show()

# bridge output for different torque values

torque_applied_a = np.linspace(1, 10, n_of_steps)
gamma_xy_a = shear_stress_torsion(T=torque_applied_a, rho=(d_out / 2), J=J)/G
displacements_sg_a = deformation_on_plane(epsilon_x=0, epsilon_y=0, gamma_xy=gamma_xy_a, theta=-strain_gauge_angle)
SG1_a = SG3_a = strain_gauge_resistance_read(strain_gauge_nominal_resistance, strain_gauge_gf, displacements_sg_a[0])
SG2_a = SG4_a = strain_gauge_resistance_read(strain_gauge_nominal_resistance, strain_gauge_gf, -displacements_sg_a[0])
bridge_reading_a = wheatstone_bridge_output(circuit_voltage, SG1_a, SG2_a, SG3_a, SG4_a)

plt.figure(figsize=(10, 8))
plt.style.use('fivethirtyeight')
plt.plot(torque_applied_a, bridge_reading_a*1e3, 'b')
plt.title('bridge voltage x torque')
plt.xlabel('torque [Nm]')
plt.ylabel('bridge voltage output [mV]')
plt.show()
