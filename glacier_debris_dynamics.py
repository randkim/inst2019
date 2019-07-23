import numpy as np

#Based on the paper by Konrad & Humphrey
#"Steady-state flow model of debris-covered glaciers (rock glaciers)"

debris_mass_balance = 1
ice_mass_balance = 1

avg_ice_velocity = 1
c_avg_ice_velocity = 1

ice_depth = 1
debris_depth = 1

z = 1

#Debris mass conservation
c_debris_mass = debris_mass_balance

#Ice mass conservation
c_ice_depth = ice_mass_balance/avg_ice_velocity - ice_depth/avg_ice_velocity * c_avg_ice_velocity


a = 4*10**-24
n = 3
density_ice = 900
density_debris = 1800
density_ratio = density_debris/density_ice
g = 9.8
theta = 15 #may have to convert to radians

constant = 2*a*(density_ice*g*np.sin(theta))**n

#Parallel-side flow model velocity
ice_velocity_surface = constant/(n+1) * ((ice_depth + density_ratio*debris_depth)**(n+1) - (z + density_ratio*debris_depth)**(n+1))

#Integrate above with respect to z for average velocity
avg_ice_velocity = constant/((n+1)(n+2)*ice_depth) * (ice_depth*(n+2)(ice_depth + density_ratio*debris_depth)**(n+1) + (density_ratio*debris_depth)**(n+2) - (ice_depth + density_ratio*debris_depth)**(n+2))