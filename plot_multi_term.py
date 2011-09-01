"""Module for plotting results of first term model."""

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import multi_term 
reload(multi_term)

cat1 = multi_term.Catalyst()

cat1.A_arr = 5576796142069.6602
cat1.T_a = 15325.877039480061
cat1.set_eta()

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

Da_range = sp.arange(0, 20, 0.01)
lambda_1_curve = cat1.get_lambda(Da_range)

# fig_eigen = plt.figure()
# plt.plot(cat1.lambda_and_Da[:,0], cat1.lambda_and_Da[:,1], 'x',
#          label='data') 
# plt.plot(Da_range, lambda_1_curve, label='fit')
# plt.xlabel('Da')
# plt.ylabel(r'$\lambda_1$')
# plt.xlim(0,1)
# plt.ylim(0,1)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(left=0.17)
# #plt.title('First Eigenvalue Spline Fit')
# plt.grid()
# plt.legend(loc='lower right')
# plt.savefig('Plots/eigen_fit.pdf')
# plt.savefig('Plots/eigen_fit.png')

# fig_species = plt.figure()
# x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)
# # TICKS = sp.arange(0,1.5,0.1)
# LEVELS = sp.arange(0, 1.2, 0.1)
# FCS = plt.contourf(x_2d, y_2d, cat1.Yxy_.T) 
# CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
# plt.grid()
# plt.xlabel(r'$\tilde{x}$')
# plt.ylabel(r'$\tilde{y}$')
# # plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
# #           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
# plt.ylim(-1, 1)
# plt.subplots_adjust(bottom=0.15)
# plt.subplots_adjust(left=0.15)
# plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.pdf') 
# plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.png')  

FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

fig_eta = plt.figure()
Pe_2d = cat1.Pe_array.T
dummy, Da_2d = np.meshgrid(cat1.Pe_array[:,0], cat1.Da_array)
TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.05, 0.05)
FCS = plt.contourf(Pe_2d, Da_2d, cat1.eta.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel('Pe')
plt.ylabel('Da')
plt.title('Species Conversion Efficiency')
plt.savefig('Plots/eta.pdf')
plt.savefig('Plots/eta.png')

plt.show()


