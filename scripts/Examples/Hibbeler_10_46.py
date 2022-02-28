"""
Find:
Strains in x' and y' strain gauges

Assume:
Shaft is only subjected to torque
"""

from numpy import cos, sin
from numpy import deg2rad
from numpy import pi


def rpm_to_rad_ps(speed_angular):
    return speed_angular * (2 * pi) / 60


def polar_inertia_circular_section(section_diameter):
    return pi*(section_diameter**4)/32


def shear_stress_torsion(torque, section_diameter):
    return torque*(section_diameter/2)/polar_inertia_circular_section(section_diameter)


def strain_deformation_plane_principal(epsilon_x=0, epsilon_y=0, gamma_xy=0, plane_angle=0):
    return ((epsilon_x + epsilon_y)/2) + ((epsilon_x - epsilon_y)/2)*cos(2*plane_angle) + (gamma_xy/2)*sin(plane_angle)


def strain_deformation_plane(epsilon_x=0, epsilon_y=0, gamma_xy=0, plane_angle=0):
    return epsilon_x*cos(plane_angle)**2 + epsilon_y*sin(plane_angle)**2 + gamma_xy*sin(plane_angle)*cos(plane_angle)


def shear_deformation_plane(epsilon_principal=0, epsilon_x=0, epsilon_y=0, plane_angle=0):
    return (2/sin(plane_angle))*(epsilon_principal - ((epsilon_x + epsilon_y)/2)
                                 - ((epsilon_x - epsilon_y)/2)*cos(2*plane_angle))


def torque_from_deformation(material_G, shaft_diameter, deformation_torsion):
    return material_G * polar_inertia_circular_section(shaft_diameter) * deformation_torsion / (shaft_diameter/2)


"""input data"""
SHAFT_DIAMETER = 30E-3  # m
SHAFT_MATERIAL_G = 75E9  # Pa
TORQUE_APPLIED = 2E3  # Nm
STRAIN_GAUGE_ANGLE = deg2rad(45)  # deg


"""solving"""
shear_stress = shear_stress_torsion(TORQUE_APPLIED, SHAFT_DIAMETER)
shear_angle = shear_stress/SHAFT_MATERIAL_G

# strain rosettes
strain_x_line = strain_deformation_plane(gamma_xy=shear_angle, plane_angle=STRAIN_GAUGE_ANGLE)
strain_y_line = strain_deformation_plane(gamma_xy=shear_angle, plane_angle=STRAIN_GAUGE_ANGLE+pi/2)

