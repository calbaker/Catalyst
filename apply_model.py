"""Script for running the model on new and exciting things."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import os


import multi_term
reload(multi_term)

plt.close('all')

cat = multi_term.Catalyst()
cat.A_arr0 = 11.29e6
cat.T_a = 6.822e3  

cat.Vdot = 500.e-6 / 60. 
cat.T = 450.

cat.thickness0 = 5.e-6

cat.thickness_array = np.linspace(1, 200, 100) * 1.e-6
cat.A_arr_array = ( cat.A_arr0 / (cat.thickness_array /
                                  cat.thickness0) )
cat.Kn_length_array = np.array([1., 5., 10., 50., 100.]) * 1.e-9

cat.eta_Pt_density = np.zeros([cat.thickness_array.size, cat.A_arr_array.size])
cat.eta_Pt_total = np.zeros([cat.thickness_array.size, cat.A_arr_array.size])

cat.Pe = cat.get_Pe(cat.Vdot, cat.T)

for j in range(cat.Kn_length_array.size):
    cat.Kn_length = cat.Kn_length_array[j]
    for i in range(cat.thickness_array.size):
        cat.thickness = cat.thickness_array[i]
        cat.A_arr = cat.A_arr_array[i]
        cat.Da = cat.get_Da(cat.T, cat.A_arr, cat.T_a)
        cat.eta_Pt_total[i,j] = cat.get_eta(cat.Pe, cat.Da)
        cat.A_arr = cat.A_arr0
        cat.Da = cat.get_Da(cat.T, cat.A_arr, cat.T_a)
        cat.eta_Pt_density[i,j] = cat.get_eta(cat.Pe, cat.Da)


# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.
plt.rcParams['lines.markersize'] = 10


FORMATTER = tic.FormatStrFormatter('%1.1f')
MARKERS = ['-k', '--b', '-.r', ':m', '-g']
LABELS = list(['1 nm', '5 nm', '10 nm', '50 nm', '100 nm'])

plt.figure()
for i in range(cat.Kn_length_array.size):
    plt.plot(cat.thickness_array * 1.e6, cat.eta_Pt_density[:,i] *
             100., MARKERS[i], label=LABELS[i]) 
plt.xlabel(r'Nanowire Height ($\mu$m)')
plt.ylabel('Conversion Efficiency (%)')
#ax1.yaxis.set_major_formatter(FORMATTER)
plt.grid()
plt.ylim(ymin=0)
plt.legend(loc='lower right',title='Knudsen Length ($\mu$m)')
plt.subplots_adjust(left=0.15)
plt.savefig('Plots/applied/eta_Pt_density.pdf')
plt.savefig('Plots/applied/eta_Pt_density.png')

plt.figure()
for i in range(cat.Kn_length_array.size):
    plt.plot(cat.thickness_array * 1.e6, cat.eta_Pt_total[:,i] *
             100., MARKERS[i], label=LABELS[i]) 
plt.xlabel(r'Nanowire Height ($\mu$m)')
plt.ylabel('Conversion Efficiency (%)')
#ax1.yaxis.set_major_formatter(FORMATTER)
plt.grid()
plt.ylim(0,20)
plt.legend(loc='lower left',title=r"Knudsen Length ($\mu$m)")
plt.subplots_adjust(left=0.15)
plt.savefig('Plots/applied/eta_Pt_total.pdf')
plt.savefig('Plots/applied/eta_Pt_total.png')

plt.show()
