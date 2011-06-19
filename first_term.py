import numpy as np
import scipy as sp

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
        self.ORDER = sp.size(self.Da_fix) - 1 - 6
        self.Da_array = sp.arange(0.1, 10., 0.1)
        self.Pe_array = sp.arange(100., 1000., 25.)
        self.length_ = 100.

    def set_fit(self):
        """Uses polynomial fit curve to represent lambda as a function
        of Da with handpicked values."""
        self.coeffs = sp.polyfit(self.Da_fix, self.lambda_1, self.ORDER)
        self.lambda_poly = sp.poly1d(self.coeffs)

    def set_Y_(self):
        """Sets float non-dimensional Y at any particular non-d x,y
        point""" 
        self.set_fit()
        Y_ = ( self.lambda_poly(self.Da) / self.lambda_poly(self.Da) *
        sp.exp(-self.lambda_poly(self.Da)**2. / (4. * self.Pe ) *
        self.x_) * sp.cos(self.lambda_poly(self.Da) * self.y_) ) 
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
    
    def set_eta(self):
        """Sets conversion efficiency over a range of Pe and Da."""
        self.eta = sp.zeros([sp.size(self.Pe_array),
        sp.size(self.Da_array)])
        for i in sp.arange(sp.size(self.Pe_array)):
            for j in sp.arange(sp.size(self.Da_array)):
                self.eta[i,j] = ( 1. - 1. /
        sp.sin(self.lambda_poly(self.Da_array[j])) *
        sp.exp(-self.lambda_poly(self.Da_array[j])**2. / (4. *
        self.Pe_array[i]) * self.length_) *
        sp.sin(self.lambda_poly(self.Da_array[j])) ) 
        

