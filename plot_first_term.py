"""Module for plotting results of first term model."""

import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
reload(ft)

cat1 = ft.One_Term_Catalyst()

cat1.x_array = np.arange(0., 1050., 50.)
cat1.y_array = np.arange(-1., 1.05, 0.05)
cat1.Da_array = sp.arange(0.05, 5., 0.05)
cat1.lambda1 = cat1.get_lambda(cat1.Da_array)
#cat1.set_Yxy_()
cat1.set_eta_dimless()

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

Da_range = sp.arange(0, 20, 0.01)
lambda_1_curve = cat1.get_lambda(Da_range)

fig_eigen = mpl.figure()
mpl.plot(cat1.lambda_and_Da[:,0], cat1.lambda_and_Da[:,1], 'x',
         label='data') 
mpl.plot(Da_range, lambda_1_curve, label='fit')
mpl.xlabel('Da')
mpl.ylabel(r'$\lambda_1$')
mpl.xlim(0,1)
mpl.ylim(0,1)
mpl.title('First Eigenvalue Spline Fit')
mpl.grid()
mpl.legend(loc='lower right')
mpl.savefig('Plots/eigen_fit.pdf')
mpl.savefig('Plots/eigen_fit.png')

# fig_species = mpl.figure()
# x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)
# # TICKS = sp.arange(0,1.5,0.1)
# LEVELS = sp.arange(0, 1.2, 0.1)
# FCS = mpl.contourf(x_2d, y_2d, cat1.Yxy_.T) 
# CB = mpl.colorbar(FCS, orientation='horizontal', format='%.2f')
# mpl.grid()
# mpl.xlabel(r'$\tilde{x}$')
# mpl.ylabel(r'$\tilde{y}$')
# mpl.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
# mpl.ylim(-1, 1)
# mpl.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.pdf') 
# mpl.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
#             + '.png')  

fig_eta = mpl.figure()
Pe_2d, Da_2d = np.meshgrid(cat1.Pe_array, cat1.Da_array)
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.05, 0.05)
FCS = mpl.contourf(Pe_2d, Da_2d, cat1.eta_dimless.T, LEVELS) 
CB = mpl.colorbar(FCS, orientation='horizontal', format='%.2f')
mpl.grid()
mpl.xlabel('Pe')
mpl.ylabel('Da')
mpl.title('Species Conversion Efficiency')
mpl.savefig('Plots/eta.pdf')
mpl.savefig('Plots/eta.png')

cat1.A_arr = 25950754583570564.0
cat1.T_a = 22056.187248619895
cat1.set_eta_dim()
Vdot2d, T2d = np.meshgrid(cat1.Vdot_array, cat1.T_array)
Vdot2d = Vdot2d * 60. * 1.e6
# converts back to sccm for plotting
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0., 1.05, 0.05)
fig_eta_real = mpl.figure()
FCS = mpl.contourf(Vdot2d, T2d, cat1.eta_dim.T, LEVELS)
CB = mpl.colorbar(FCS, orientation='horizontal')
mpl.grid()
mpl.xlabel(r'$\dot{V}$ (sccm)')
mpl.ylabel('T (K)')
mpl.title(
    'Conversion Efficiency v.\nFlow Rate and Temperature') 
mpl.savefig('Plots/real eta.pdf')
mpl.savefig('Plots/real eta.png')

mpl.show()


