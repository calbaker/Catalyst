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

cat.thickness_array = np.linspace(1, 1000, 10) * 1.e-6
cat.A_arr_array = ( cat.A_arr0 / (cat.thickness_array / cat.thickness0) )

# cat.eta2d = np.zeros([cat.thickness_array.size, cat.A_arr_array.size])

cat.eta = np.zeros(cat.thickness_array.size)

for i in range(cat.eta.size):
    cat.A_arr = cat.A_arr_array[i]
    cat.thickness = cat.thickness_array[i]
    cat.Pe = cat.get_Pe(cat.Vdot, cat.T)
    cat.Da = cat.get_Da(cat.T, cat.A_arr, cat.T_a)
    cat.eta[i] = cat.get_eta(cat.Pe, cat.Da)

# cat.total_Pt0 = cat.A_arr0 * cat.thickness0

# for i in range(cat.eta2d.shape[0]):
#     cat.thickness = cat.thickness_array[i]
#     for j in range(cat.A_arr_array.size):
#         cat.A_arr = cat.A_arr_array[j]
#         cat.Pe = cat.get_Pe(cat.Vdot, cat.T)
#         cat.Da = cat.get_Da(cat.T, cat.A_arr, cat.T_a)
#         cat.eta2d[i,j] = cat.get_eta(cat.Pe, cat.Da)

# cat.Pt_normal = ( cat.A_arr / cat.A_arr0 * cat.thickness /
#                   cat.thickness0 )
# cat.eta_normal = cat.eta2d / cat.Pt_normal
# cat.eta_normal = cat.eta_normal / cat.eta_normal.max()

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

# X,Y = np.meshgrid(cat.thickness_array * 1e6, A_arr_nondim) 

# LEVELS = np.linspace(0,0.56,15)

# plt.figure()
# FCS = plt.contourf(X, Y, cat.eta2d, levels=LEVELS) 
# CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
# CB.set_label("Conversion Efficiency")
# plt.xlabel(r'Washcoat Thickness ($\mu$m)')
# plt.ylabel('Normalized Pt/Pd Loading')

# min = np.log10(cat.eta_normal.min())
# max = np.log10(cat.eta_normal.max())
# LEVELS = (cat.eta_normal.max() - np.logspace(max,min,24) + 10.**min)

# #LEVELS = np.linspace(0.5, 1, 12) * cat.eta_normal.max()

# plt.figure()
# FCS = plt.contourf(X, Y, cat.eta_normal, levels=LEVELS) 
# CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
# CB.set_label("Normalized Conversion Efficiency")
# plt.xlabel(r'Washcoat Thickness ($\mu$m)')
# plt.ylabel('Normalized Pt/Pd Loading')


FORMATTER = tic.FormatStrFormatter('%1.1f')

plt.figure()
ax1 = plt.subplot(111)
plt.plot(cat.thickness_array * 1.e6, cat.eta * 100.)
plt.xlabel(r'Nanowire Height ($\mu$m)')
plt.ylabel('Conversion Efficiency (%)')
ax1.yaxis.set_major_formatter(FORMATTER)
plt.grid()
plt.savefig('Plots/eta_applied.pdf')
plt.savefig('Plots/eta_applied.png')
plt.subplots_adjust(left=0.15)

plt.show()
