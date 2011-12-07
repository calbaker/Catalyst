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


cat.thickness_array = np.linspace(1,100,50)
cat.eta_t = np.zeros(cat.thickness.size)

for i in range(cat.eta_t.shape[0])):
    cat.thickness cat.thickness_array[i]
    cat.set_eta()
    cat.eta_t[i] = cat.eta 

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.plot(cat.thickness * 1.e6, cat.eta_t)
plt.xlabel(r'Nanowire Height ($\mu$m)')
plt.ylabel('Conversion Efficiency')
plt.grid()
plt.savefig('Plots/eta_applied.pdf')
plt.savefig('Plots/eta_applied.png')
