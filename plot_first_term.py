"""Module for plotting results of first term model."""

import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *
    
cat1 = One_Term_Catalyst()

cat1.x_array = np.arange(0., 1050., 50.)
cat1.y_array = np.arange(-1., 1.01, 0.01)
cat1.set_Yxy_()

# Plot configuration
x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)

FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

Da_range = sp.arange(0, 41, 1.)
lambda_1_curve = cat1.lambda_poly(Da_range)

fig1 = mpl.figure()
mpl.plot(cat1.Da_fix, cat1.lambda_1, 'x', label='data')
mpl.plot(Da_range, lambda_1_curve, label='fit')
mpl.xlabel('Da')
mpl.ylabel(r'$\lambda_1$')
mpl.ylim(0,2)
mpl.title('First Eigenvalue Polynomial Fit\nOrder='+str(cat1.ORDER))
mpl.grid()
mpl.legend()
mpl.savefig('Plots/eigen_fit.pdf')
mpl.savefig('Plots/eigen_fit.png')

fig_eta = mpl.figure()
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
FCS = mpl.contourf(x_2d, y_2d, cat1.Yxy_.T) 
CB = mpl.colorbar(FCS, orientation='horizontal', format='%.2f')
mpl.grid()
mpl.xlabel(r'$\tilde{x}$')
mpl.ylabel(r'$\tilde{y}$')
mpl.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
          '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
mpl.ylim(-1, 1)
mpl.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.pdf') 
mpl.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.png')  

mpl.show()


