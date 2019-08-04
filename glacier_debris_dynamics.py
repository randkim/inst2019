import numpy as np
import matplotlib.pyplot as plt
import random as rd

#Initial Conditions
debris_temp_surface = [278]
debris_temp_btm = [276]
ice_temp = [272.995]
night_temp_min = 260
night_temp_max = 275

#Constants
density_ice = 917 #kg/m^3,Cutnell, John D., & Kenneth W. Johnson. Physics, 3rd Edition. New York: Wiley, 1995: 315
heatcap_ice = 2050 #https://www.engineeringtoolbox.com/ice-thermal-properties-d_576.html
latent_fusion = 333.55*1000 #https://en.wikipedia.org/wiki/Enthalpy_of_fusion
density_rock = 2500 #https://www.eoas.ubc.ca/ubcgif/iag/foundations/properties/density.htm
heatcap_rock = 2000 #https://www.e-education.psu.edu/earth103/node/1005

#https://www.engineeringtoolbox.com/thermal-conductivity-d_429.html
thermal_conductivity_of_rock = 5

#https://www.engineersedge.com/heat_transfer/convective_heat_transfer_coefficients__13378.htm
heat_transfer_coefficient_air = 26
heat_transfer_coefficient_water = 260

soil_albedo = 0.17
solar_constant = 1400


#Lists
debris_depth = list(range(0, 10))
R_rock = debris_depth[-1]/thermal_conductivity_of_rock
surface_temp_gradient = []
bottom_temp_gradient = []
avg_temp_gradient = []
avg_temp = []


ice_mass = [-4.525*10**(-5)]

#While ice is below melting temperature, ice first heats up to 273 Kelvin, the melting temperature
while ice_temp[-1] <= 273:
    night_solar_constant = rd.randint(-5000, 0)
    #Step 1: Day - Solar radiation heats up the top surface of the debris layer
    if rd.randint(0,10) <= 5: #day
        change_debris_surface_temp = (1 - soil_albedo) * solar_constant/(density_rock * heatcap_rock)
        print('day0', change_debris_surface_temp)

        #print('day ' + str(change_debris_surface_temp))

    #Step 1: Night - Air either convects heat to or from the surface of the debris layer
    else: #night
        change_debris_surface_temp = night_solar_constant/(density_rock * heatcap_rock)
        print('night0', change_debris_surface_temp)
        #change_debris_surface_temp = (air_temp[-1] - debris_temp_surface[-1])/R_rock #negative value
        #print('night ' + str(change_debris_surface_temp))

    #Step 2: Update debris temperatures. The heat at the surface is assumed to transfer as 1/d to the bottom surface.
    debris_temp_surface.append(debris_temp_surface[-1] + change_debris_surface_temp)
    debris_temp_btm.append(debris_temp_btm[-1] + change_debris_surface_temp/max(debris_depth))

    #Step 3: Two thermal gradients form. One from the updated surface temperature to the bottom, and another from the botton (which is at ice temperature) to the surface. Take the average as the actual gradient.
    for i in range(len(debris_depth)):
        surface_temp_gradient.append(-thermal_conductivity_of_rock * debris_depth[i] + debris_temp_surface[-1])
        bottom_temp_gradient.append(-thermal_conductivity_of_rock * debris_depth[i] + debris_temp_btm[-1])

    for i in range(len(surface_temp_gradient)):
        avg_temp_gradient.append((surface_temp_gradient[i] + bottom_temp_gradient[i])/2)

    hi = change_debris_surface_temp

    avg_temp.append(np.average(avg_temp_gradient))

# =============================================================================
#         if avg_temp_gradient[i] - surface_temp_gradient[i] != 0:
#             print("Valid")
# =============================================================================

    # =============================================================================
    # plt.plot(surface_temp_gradient, debris_depth)
    # plt.plot(bottom_temp_gradient, debris_depth)
    # plt.plot(avg_temp_gradient, debris_depth)
    # =============================================================================

    #Step 3: Ice temperature increases
    change_ice_temp = thermal_conductivity_of_rock * (debris_temp_btm[-1] - ice_temp[-1])/(density_ice * heatcap_ice)
    ice_temp.append(ice_temp[-1] + change_ice_temp)
    print(ice_temp[-1])


#Once ice heats up to melting temperature
if ice_temp[-1] > 273:

    while np.abs(ice_mass[-1]) < 4.530*10**(-5):
        night_solar_constant = rd.randint(-1400, 1400)
        if rd.randint(0,10) <= 5: #day
            change_debris_surface_temp = (1 - soil_albedo) * solar_constant/(density_rock * heatcap_rock)
            print('day', change_debris_surface_temp)

        else: #night
            change_debris_surface_temp = night_solar_constant/(density_rock * heatcap_rock)
            print('night', change_debris_surface_temp)

        debris_temp_surface.append(debris_temp_surface[-1] + change_debris_surface_temp)
        debris_temp_btm.append(debris_temp_btm[-1] + change_debris_surface_temp/max(debris_depth))

        for i in range(len(debris_depth)):
            surface_temp_gradient.append(-thermal_conductivity_of_rock * debris_depth[i] + debris_temp_surface[-1])
            bottom_temp_gradient.append(-thermal_conductivity_of_rock * debris_depth[i] + debris_temp_btm[-1])

        for i in range(len(surface_temp_gradient)):
            avg_temp_gradient.append((surface_temp_gradient[i] + bottom_temp_gradient[i])/2)

        avg_temp.append(np.average(avg_temp_gradient))
# =============================================================================
#             if avg_temp_gradient[i] - surface_temp_gradient[i] != 0:
#                 print("Hi")
# =============================================================================

        #Step 3: Ice mass loss calculation
        ice_mass_loss = - thermal_conductivity_of_rock * (debris_temp_btm[-1] -ice_temp[-1])/latent_fusion
        ice_mass.append(ice_mass_loss)

        ice_temp.append(ice_temp[-1])

fig, axs = plt.subplots(2,2)

axs[0,0].plot(range(len(ice_mass)),ice_mass)
axs[0,0].set_title("Loss in ice mass per iteration")

axs[0,1].plot(range(len(ice_temp)), ice_temp)
axs[0,1].set_title("Change in ice temperature until melting point")

axs[1,0].plot(range(len(avg_temp)), avg_temp)
axs[1,0].set_title("Change in average debris layer temperature per iteration")

#axs[1,1].plot(range(len(surface_temp_gradient)), surface_temp_gradient)
plt.show()
