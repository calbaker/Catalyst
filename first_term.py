import numpy as np
import scipy as sp
import matplotlib.pyplot as mpl

class One_Term_Catalyst():
    """Class for representing catalyst reactor modeled by 1 term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
        self.Da = 1.
        self.Pe = 500.
        self.Da_fix = ( sp.array([0.1, 0.5, 1., 2., 5., 10., 15., 20.,
        30., 40., 50.]) )   
        self.lambda_1 = ( sp.array([0.31, 0.65, 0.86, 1.08, 1.31,
        1.43, 1.47, 1.50, 1.52, 1.53, 1.54]) )     
        self.ORDER = sp.size(Da_fix) - 1 - 4

    def set_fit(self):
        """Uses polynomial fit curve to represent lambda as a function
        of Da with handpicked values."""
        self.coeffs = sp.polyfit(Da_fix, lambda_1, ORDER)
        self.lambda_poly = sp.poly1d(coeffs)

    def set_Y_(self):
        """Sets float non-dimensional Y at any particular non-d x,y
        point""" 
        self.set_fit()
        Y_ = ( 2. * self.lambda_poly(Da) / self.lambda_poly(Da) *
        sp.exp(-self.lambda_poly(Da)**2. / (4. * self.Pe ) * self.x_) *
        sp.cos(self.lambda_poly(Da) * self.y_) )
        return Y_

    def set_Yxy_(self):
        """Sets non-dimensional Y over a 2d array of non-dimensional
        x_ and y_"""
        self.Yxy_ = np.zeros([np.size(self.x_array),
        np.size(self.y_array)])

        for i in sp.arange(sp.size(self.x_array)):
            for j in sp.arange(sp.size(self.y_array)):
                self.x_ = self.x_array[i]
                self.y_ = self.y_array[j]
                self.Yxy_[i,j] = self.set_Y_()
    
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
lambda_1_curve = lambda_poly(Da_range)

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

fig_eta = mpl.figure()
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
FCS = mpl.contourf(x_2d, y_2d, cat1.Yxy_.T) 
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


