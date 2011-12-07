"""Module for class definition for experimental data with model curve
fitting capability."""

import numpy as np
from scipy.optimize import curve_fit

import multi_term
import first_term

class ExpData(object):
    """Class for keeping track of experimental data"""

    def __init__(self):
        """Sets constants and initializes parent class."""
        self.T_ambient = 300. # ambient temperature (K)
        self.p0 = np.array([5.e16, 27.e3])

    def set_params(self):
        """Uses scipy optimize curve_fit to determine Arrhenius
        parameters that result in best curve fit."""
        popt, pcov = curve_fit(self.get_eta_dim, self.T_exp,
        self.eta_exp, p0 = self.p0) 
        self.A_arr = popt[0]
        self.T_a = popt[1]
        self.set_eta()

    def get_eta_dim(self, T, A_arr, T_a):
        """Returns species conversion efficiency, eta, as a function
        of required argument T. Used by set_params."""
        self.Pe_ij = self.get_Pe(self.Vdot,T) 
        Da = self.get_Da(T, A_arr, T_a)
        eta = self.get_eta(self.Pe_ij, Da)
        return eta

    def get_S_r(self):
        """Returns sum of residuals squared for all data points."""
        S_r = np.sum((self.eta_model - self.eta_exp)**2.)
        return S_r
        
class ExpDataMulti(ExpData,multi_term.Catalyst):
    """Class for handling experimental calibration of the multiterm
    catalyst model."""

    def __init__(self):
        """This should initialize both parent classes."""
        self.__class__.__mro__[1].__init__(self)
        self.__class__.__mro__[2].__init__(self)        
