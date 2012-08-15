"""Generates two contour plots for species concentration in two
dimensions, one for first term and one for multi term."""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst
reload(catalyst)

x_array = np.linspace(0., 30., 100)
y_array = np.linspace(0, 1., 50)

Pe = 50.
Da = 0.1
# reasonable Pe and Da for experimental conditions are Pe = 20 to 50
# and Da = 0.01 to 0.15

cat4 = catalyst.Catalyst()
cat4.x_array = x_array
cat4.y_array = y_array
cat4.Pe = Pe
cat4.Da = Da
cat4.Yxy = np.zeros([x_array.size, y_array.size])

cat1 = catalyst.Catalyst(terms=1)
cat1.x_array = x_array
cat1.y_array = y_array
cat1.Pe = Pe
cat1.Da = Da
cat1.Yxy = np.zeros([x_array.size, y_array.size])

cat_num = catalyst.Catalyst()
cat_num.Pe = Pe
cat_num.Da = Da
cat_num.x_array = x_array
cat_num.y_array = y_array
cat_num.solve_numeric()

for i in range(x_array.size):
    x_ = x_array[i]
    for j in range(y_array.size):
        y_ = y_array[j]

        cat4.Yxy[i, j] = cat4.get_Y(x_, y_, Pe=Pe, Da=Da)
        cat1.Yxy[i, j] = cat1.get_Y(x_, y_, Pe=Pe, Da=Da)

cat4.Yxy = np.concatenate((cat4.Yxy[:, ::-1][:, 1:], cat4.Yxy), 1)
cat1.Yxy = np.concatenate((cat1.Yxy[:, ::-1][:, 1:], cat1.Yxy), 1)
cat_num.Yxy_num = np.concatenate((cat_num.Yxy_num[:, ::-1][:, 1:], cat_num.Yxy_num), 1)

y_array = np.concatenate((-y_array[1:][::-1], y_array), 0)

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

TICKS = np.arange(0, 1.2, 0.2)
LEVELS = np.arange(0, 1.1, 0.1)

plt.close()

x_2d, y_2d = np.meshgrid(x_array, y_array)
fig_eta = plt.figure('4 terms')
FCS = plt.contourf(x_2d, y_2d, cat4.Yxy.T)#, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical')#, ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/species4 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig('../Plots/species4 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.png')

fig_species = plt.figure('1 term')
# TICKS = np.arange(0,1.5,0.1)
LEVELS = np.arange(0, 1.2, 0.1)
FCS = plt.contourf(x_2d, y_2d, cat1.Yxy.T)# , levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')# , ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/species1 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig('../Plots/species1 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.png')

fig_species = plt.figure('numerical')
FCS = plt.contourf(x_2d, y_2d, cat_num.Yxy_num.T)
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/species num Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig('../Plots/species num Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.png')

plt.show()
