"""
Find:
Strains in x' and y' strain gauges

Assume:
Strain gauge is in the flex moment neutral plane (sigma_x = 0)
"""

from numpy import cos, sin
from numpy import deg2rad
from numpy import pi


def tube_section_polar_inertia(tube_diameter_inner, tube_diameter_outer):
    return pi*((tube_diameter_outer**4) - (tube_diameter_inner**4))/32


def tube_section_inertia(tube_diameter_inner, tube_diameter_outer):
    return pi*((tube_diameter_outer**4) - (tube_diameter_inner**4))/64


def tube_section_inertia_first(tube_diameter_inner, tube_diameter_outer):
    return 4*((tube_diameter_outer/2)**3 - (tube_diameter_inner/2)**3)/6


def shear_deformation_pure_plane(epsilon_principal=0., epsilon_x=0., epsilon_y=0., plane_angle=0.):
    return (epsilon_principal - epsilon_x - epsilon_y)/(sin(plane_angle)*cos(plane_angle))


"""input data"""
SECTION_DIAMETER_OUTER = 25E-3  # m
SECTION_DIAMETER_INNER = 15E-3  # m
TUBE_L_LENGTH = 150E-3  # m
TUBE_A_LENGTH_TO_SG = 200E-3  # m
TUBE_MATERIAL_G = 38E9  # GPa
STRAIN_GAUGE_READING = -250E-6
STRAIN_GAUGE_ANGLE = deg2rad(60)


""""solving"""
shear = shear_deformation_pure_plane(epsilon_principal=STRAIN_GAUGE_READING,
                                     plane_angle=STRAIN_GAUGE_ANGLE)

Q_A = tube_section_inertia_first(tube_diameter_inner=SECTION_DIAMETER_INNER, tube_diameter_outer=SECTION_DIAMETER_OUTER)
I_z = tube_section_inertia(tube_diameter_inner=SECTION_DIAMETER_INNER, tube_diameter_outer=SECTION_DIAMETER_OUTER)
J = tube_section_polar_inertia(tube_diameter_inner=SECTION_DIAMETER_INNER, tube_diameter_outer=SECTION_DIAMETER_OUTER)
b_a = SECTION_DIAMETER_OUTER - SECTION_DIAMETER_INNER

load = (TUBE_MATERIAL_G*shear)/(Q_A/(I_z*b_a) - TUBE_L_LENGTH*(SECTION_DIAMETER_OUTER/2)/J)

print(TUBE_MATERIAL_G*shear)
print(Q_A/(I_z*b_a))
print(TUBE_L_LENGTH*(SECTION_DIAMETER_OUTER/2)/J)
print(load)

