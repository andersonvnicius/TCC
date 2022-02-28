"""
Find:
Applied torque at the shaft

Assume:
Shaft is only subjected to torque
"""

from numpy import cos, sin
from numpy import deg2rad
from numpy import pi


def rpm_to_rad_ps(speed_angular):
    return speed_angular * (2 * pi) / 60


def stress_deformation_principal(epsilon_x=0, epsilon_y=0, gamma_xy=0, plane_angle=0):
    return ((epsilon_x + epsilon_y)/2) + ((epsilon_x - epsilon_y)/2)*cos(2*plane_angle) + (gamma_xy/2)*sin(plane_angle)


def shear_deformation_plane(epsilon_principal=0, epsilon_x=0, epsilon_y=0, plane_angle=0):
    return (2/sin(plane_angle))*(epsilon_principal - ((epsilon_x + epsilon_y)/2)
                                 - ((epsilon_x - epsilon_y)/2)*cos(2*plane_angle))


def torque_from_deformation(material_G, shaft_diameter, deformation_torsion):
    return material_G * (pi*(shaft_diameter**4)/32) * deformation_torsion / (shaft_diameter/2)


"""input data"""
SHAFT_DIAMETER = 25E-3  # m
SHAFT_MATERIAL_G = 75E9  # Pa
SHAFT_SPEED_ANGULAR = rpm_to_rad_ps(1760)  # radps
STRAIN_GAUGE_READING = 800E-6  #
STRAIN_GAUGE_ANGLE = deg2rad(60)  # deg


"""solving"""
torsional_deformation_angle = shear_deformation_plane(epsilon_principal=STRAIN_GAUGE_READING,
                                                      epsilon_x=0, epsilon_y=0,
                                                      plane_angle=STRAIN_GAUGE_ANGLE)

torque = torque_from_deformation(SHAFT_MATERIAL_G, SHAFT_DIAMETER, torsional_deformation_angle)
power = torque*SHAFT_SPEED_ANGULAR

"""prints"""
# print(torsional_deformation_angle)
# print(torque)
# print(power)

