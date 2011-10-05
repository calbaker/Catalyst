import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term
reload(first_term)
import multi_term 
reload(multi_term)

x_array = np.linspace(0., 100., 100)
y_array = np.linspace(-1., 1., 100)

Pe = 50.
Da = 1.

cat4 = multi_term.Catalyst()
cat4.x_array = x_array
cat4.y_array = y_array
cat4.Pe = Pe
cat4.Da = Da
cat4.set_Yxy(Pe,Da)

cat1 = first_term.One_Term_Catalyst()
cat1.x_array = x_array
cat1.y_array = y_array
cat1.Pe = Pe
cat1.Da = Da
cat1.set_Yxy(Pe,Da)


# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

TICKS = sp.arange(0,1.2,0.2)
LEVELS = sp.arange(0, 1.1, 0.1)

x_2d, y_2d = np.meshgrid(x_array, y_array)
fig_eta = plt.figure()
FCS = plt.contourf(x_2d, y_2d, cat4.Yxy.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1,1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$') 
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('Plots/4species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.pdf') 
plt.savefig('Plots/4species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.png')  

fig_species = plt.figure()
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
FCS = plt.contourf(x_2d, y_2d, cat1.Yxy.T, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.pdf') 
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.png')  

plt.show()
