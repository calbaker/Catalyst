"""Module for plotting results of first term model."""

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
reload(ft)

cat1 = ft.One_Term_Catalyst()

cat1.x_array = np.arange(0., 1050., 50.)
cat1.y_array = np.arange(-1., 1.05, 0.05)
cat1.Da_array = sp.arange(0.05, 5., 0.05)
cat1.lambda1 = cat1.get_lambda(cat1.Da_array)
cat1.A_arr = 5576796142069.6602
cat1.T_a = 15325.877039480061
#cat1.set_Yxy_()
cat1.set_eta_dimless()

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

Da_range = sp.arange(0, 20, 0.01)
lambda_1_curve = cat1.get_lambda(Da_range)

fig_eigen = plt.figure()
plt.plot(cat1.lambda_and_Da[:,0], cat1.lambda_and_Da[:,1], 'x',
         label='data') 
plt.plot(Da_range, lambda_1_curve, label='fit')
plt.xlabel('Da')
plt.ylabel(r'$\lambda_1$')
plt.xlim(0,1)
plt.ylim(0,1)
plt.title('First Eigenvalue Spline Fit')
plt.grid()
plt.legend(loc='lower right')
# plt.savefig('Plots/eigen_fit.pdf')
# plt.savefig('Plots/eigen_fit.png')

# fig_species = plt.figure()
# x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)
# # TICKS = sp.arange(0,1.5,0.1)
# LEVELS = sp.arange(0, 1.2, 0.1)
# FCS = plt.contourf(x_2d, y_2d, cat1.Yxy_.T) 
# CB = plt.colorbar(FCS, orientation='horizontal', format='%.2f')
# plt.grid()
# plt.xlabel(r'$\tilde{x}$')
# plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
# plt.ylim(-1, 1)
# # plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.pdf') 
# # plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.png')  

fig_eta = plt.figure()
Pe_2d, Da_2d = np.meshgrid(cat1.Pe_array, cat1.Da_array)
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.05, 0.05)
FCS = plt.contourf(Pe_2d, Da_2d, cat1.eta_dimless.T, LEVELS) 
CB = plt.colorbar(FCS, orientation='horizontal', format='%.2f')
plt.grid()
plt.xlabel('Pe')
plt.ylabel('Da')
plt.title('Species Conversion Efficiency')
# plt.savefig('Plots/eta.pdf')
# plt.savefig('Plots/eta.png')

cat1.A_arr = 25950754583570564.0
cat1.T_a = 22056.187248619895
cat1.set_eta_dim()
Vdot2d, T2d = np.meshgrid(cat1.Vdot_array, cat1.T_array)
Vdot2d = Vdot2d * 60. * 1.e6
# converts back to sccm for plotting
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0., 1.05, 0.05)
fig_eta_real = plt.figure()
FCS = plt.contourf(Vdot2d, T2d, cat1.eta_dim.T, LEVELS)
CB = plt.colorbar(FCS, orientation='horizontal')
plt.grid()
plt.xlabel(r'$\dot{V}$ (sccm)')
plt.ylabel('T (K)')
plt.title(
    'Conversion Efficiency v.\nFlow Rate and Temperature') 
# plt.savefig('Plots/real eta.pdf')
# plt.savefig('Plots/real eta.png')

plt.show()


