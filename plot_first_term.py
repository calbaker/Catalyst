"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *

mpl.close('all')
    
cat1 = One_Term_Catalyst()

cat1.x_array = np.arange(0., 1050., 50.)
cat1.y_array = np.arange(-1., 1.01, 0.01)
cat1.Da_array = sp.arange(0.05, 5., 0.05)
cat1.set_lambda(cat1.Da_array)
#cat1.set_Yxy_()
cat1.set_eta()

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

Da_range = sp.arange(0, 41, 1.)
lambda_1_curve = cat1.set_lambda(Da_range)

fig_eigen = mpl.figure()
mpl.plot(cat1.Da_fix, cat1.lambda_1, 'x', label='data')
mpl.plot(Da_range, lambda_1_curve, label='fit')
mpl.xlabel('Da')
mpl.ylabel(r'$\lambda_1$')
mpl.ylim(0,2)
mpl.title('First Eigenvalue Polynomial Fit\nOrder='+str(cat1.ORDER))
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
FCS = mpl.contourf(Pe_2d, Da_2d, cat1.eta.T, LEVELS) 
CB = mpl.colorbar(FCS, orientation='horizontal', format='%.2f')
mpl.grid()
mpl.xlabel('Pe')
mpl.ylabel('Da')
mpl.title('Species Conversion Efficiency')
mpl.savefig('Plots/eta.pdf')
mpl.savefig('Plots/eta.png')

cat1.set_Da()
cat1.set_Pe()
cat1.set_eta_dimensional()
Vdot2d, T2d = np.meshgrid(cat1.Vdot, cat1.T_array)
Vdot2d = Vdot2d * 60. * 1.e6
# converts back to sccm for plotting
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0.6, 1.01, 0.01)
fig_eta_real = mpl.figure()
FCS = mpl.contourf(Vdot2d, T2d, cat1.eta_ij.T)
CB = mpl.colorbar(FCS, orientation='horizontal')
mpl.grid()
mpl.xlabel(r'$\dot{V}$ (sccm)')
mpl.ylabel('T (K)')
mpl.title(
    'Conversion Efficiency v.\nFlow Rate and Temperature') 
mpl.savefig('Plots/real eta.pdf')
mpl.savefig('Plots/real eta.png')

mpl.show()


