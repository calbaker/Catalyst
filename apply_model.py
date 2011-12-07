"""Script for running the model on new and exciting things."""

import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import multi_term
reload(multi_term)

plt.close('all')

cat = multi_term.Catalyst()
cat.T_a = 7207.
cat.A_arr = 1.005e7

cat.Vdot = 500.e-6 / 60. 
cat.T = 450.

cat.thickness_array = np.linspace(1,150,50) * 1.e-6
cat.eta_t = np.zeros(cat.thickness_array.size)

for i in range(cat.eta_t.shape[0]):
    cat.thickness = cat.thickness_array[i]
    cat.Pe = cat.get_Pe(cat.Vdot, cat.T)
    cat.Da = cat.get_Da(cat.T, cat.A_arr, cat.T_a)
    cat.eta_t[i] = cat.get_eta(cat.Pe, cat.Da)

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.plot(cat.thickness_array * 1.e6, cat.eta_t)
plt.xlabel(r'Nanowire Height ($\mu$m)')
plt.ylabel('Conversion Efficiency')
plt.grid()
plt.savefig('Plots/eta_applied.pdf')
plt.savefig('Plots/eta_applied.png')
