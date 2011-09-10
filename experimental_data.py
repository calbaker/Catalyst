"""Module for class definition for experimental data with model curve
fitting capability."""

import scipy as sp
from scipy.optimize import curve_fit

class ExpData():
    """Class for keeping track of experimental data"""

    def __init__(self):
        """Sets constants and initializes parent class."""
        self.T_ambient = 300. # ambient tempearture (K)
        self.CtoK = 273.15 # conversion from Celsisus to Kelvin
        self.p0 = sp.array([5.e16, 27.e3])

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
        eta = self.get_eta(Da)
        return eta

    def get_S_r(self):
        """Returns sum of residuals squared for all data points."""
        S_r = sp.sum((self.eta_model - self.eta_exp)**2.)
        return S_r
        
