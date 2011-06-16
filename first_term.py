import numpy as np
import scipy as sp
import matplotlib.pyplot as mpl

Da_fix = ( sp.array([0.1, 0.5, 1., 2., 5., 10., 15., 20., 30., 40., 50.])
       )  
lambda_1 = ( sp.array([0.31, 0.65, 0.86, 1.08, 1.31, 1.43, 1.47, 1.50,
                       1.52, 1.53, 1.54]) )     
ORDER = sp.size(Da_fix) - 1 - 4
coeffs = sp.polyfit(Da_fix, lambda_1, ORDER)
lambda_poly = sp.poly1d(coeffs)
Da_range = sp.arange(0, 41, 1.)
lambda_1_curve = lambda_poly(Da_range)

Da = 0.1
Pe = 500. 

def get_Y(x_, y_, Da, Pe):
    Y = ( 2. * lambda_poly(Da) / lambda_poly(Da) *
    sp.exp(-lambda_poly(Da)**2. / (4. * Pe ) * x_) *
    sp.cos(lambda_poly(Da) * y_) )
    return Y

x_ = np.arange(0., 1050., 50.)
y_ = np.arange(-1., 1.01, 0.01)
Y = np.zeros([np.size(x_), np.size(y_)])

for i in sp.arange(sp.size(x_)):
    for j in sp.arange(sp.size(y_)):
        Y[i,j] = get_Y(x_[i], y_[j], Da, Pe)
    

# Plot configuration
x_2d, y_2d = np.meshgrid(x_, y_)

FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

fig1 = mpl.figure()
mpl.plot(Da_fix, lambda_1, 'x', label='data')
mpl.plot(Da_range, lambda_1_curve, label='fit')
mpl.xlabel('Da')
mpl.ylabel(r'$\lambda_1$')
mpl.ylim(0,2)
mpl.title('First Eigenvalue Polynomial Fit\nOrder='+str(ORDER))
mpl.grid()
mpl.legend()
mpl.savefig('Plots/eigen_fit.pdf')
mpl.savefig('Plots/eigen_fit.png')

# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
fig_eta = mpl.figure()
FCS = mpl.contourf(x_2d, y_2d, Y.T) 
CB = mpl.colorbar(FCS, orientation='horizontal', format='%.2f')
mpl.grid()
mpl.xlabel(r'$\tilde{x}$')
mpl.ylabel(r'$\tilde{y}$')
mpl.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
          '\nDa=' + str(Da) + ' Pe=' + str(Pe))  
mpl.ylim(-1, 1)
mpl.savefig('Plots/species Da=' + str(Da) + ' Pe=' + str(Pe) + '.pdf')
mpl.savefig('Plots/species Da=' + str(Da) + ' Pe=' + str(Pe) + '.png') 

mpl.show()


