"""Module for plotting results of first term model."""


import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term 
reload(first_term)

cat1 = first_term.One_Term_Catalyst()

cat1.x_array = np.linspace(0., 100., 100)
cat1.y_array = np.linspace(-1., 1., 100)
cat1.A_arr = 5576796142069.6602
cat1.T_a = 15325.877039480061
cat1.T_array = np.linspace(300., 425., 50)
cat1.Vdot_array = np.linspace(100., 1000., 50) * 1.e-6 / 60. 
cat1.set_eta()
cat1.Pe = 500.
cat1.Da = 1.
cat1.set_Yxy(cat1.Pe,cat1.Da)

Da_range = np.linspace(0, 5., 100)
lambda_fit = cat1.get_lambda(Da_range)

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

fig_eigen = plt.figure()
plt.plot(Da_range, lambda_fit, label='fit')
plt.xlabel('Da')
plt.ylabel(r'$\lambda_1$')
plt.xlim(0,5)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.17)
#plt.title('Four Eigenvalue Spline Fit')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/4eigen_fit.pdf')
plt.savefig('Plots/4eigen_fit.png')

fig_species = plt.figure()
x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)
# TICKS = np.arange(0,1.5,0.1)
LEVELS = np.arange(0, 1.2, 0.1)
FCS = plt.contourf(x_2d, y_2d, cat1.Yxy.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' cat1.Pe=' + str(cat1.cat1.Pe))  
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.pdf') 
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.png')  

fig_eta = plt.figure()
cat1.Pe_2d = cat1.Pe_array.T
dummy, cat1.Da_2d = np.meshgrid(cat1.Pe_array[:,0], cat1.Da_array)
TICKS = np.arange(0,1.5,0.1)
LEVELS = np.arange(0, 1.05, 0.05)
FCS = plt.contourf(cat1.Pe_2d, cat1.Da_2d, cat1.eta.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(right=0.75)
plt.xlabel('Pe')
plt.ylabel('Da')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/eta.pdf')
plt.savefig('Plots/eta.png')

fig_eta_dim = plt.figure()
cat1.Vdot_2d, cat1.T_2d = np.meshgrid(cat1.Vdot_array, cat1.T_array)
TICKS = np.arange(0,1.5,0.1)
LEVELS = np.arange(0, 1.05, 0.05)
FCS = plt.contourf(cat1.Vdot_2d * 60. * 1.e6, cat1.T_2d, cat1.eta.T) 
CB = plt.colorbar(FCS, orientation='vertical')#, format='%.2f')
plt.grid()
plt.xlabel('Vdot')
plt.ylabel('T')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/eta_dim.pdf')
plt.savefig('Plots/eta_dim.png')

plt.show()


