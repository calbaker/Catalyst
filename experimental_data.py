"""Module for class definition for experimental data with model curve
fitting capability."""

import scipy as sp
from scipy.optimize import curve_fit

import first_term as ft
reload(ft)

class Data(ft.One_Term_Catalyst):
    """Class for keeping track of experimental data"""

    def __init__(self):
        """Sets constants and initializes parent class."""
        self.T_ambient = 300. # ambient tempearture (K)
        self.CtoK = 273.15 # conversion from Celsisus to Kelvin
        self.p0 = sp.array([5.e16, 27.e3])
        ft.One_Term_Catalyst.__init__(self)

    def set_eta(self):
        """Sets conversion efficiency based on inlet and oulet HC
    concentration from experiment and model for a range of
    temperatures. Vdot and T_array must be set for this to work.  It
        also does errorbar magnitude and average for several data
        points.""" 
        self.eta_raw = sp.zeros(self.HCin.shape)
        self.eta_mean = sp.zeros(self.HCin.shape[0])
        self.errorbar = sp.zeros(self.HCin.shape[0])
        
        for i in sp.arange(self.HCin.shape[0]):
            for j in sp.arange(self.HCin.shape[1]):
                self.eta_raw[i,j] = ( (self.HCin[i,j] -
        self.HCout[i,j]) / self.HCin[i,j] )
            self.eta_mean[i] = ( self.eta_raw[i,:].sum() /
            self.HCin.shape[1] )  
            self.errorbar[i] = 3.2 * self.eta_raw[i,:].std() 

    def set_params(self):
        """Uses scipy optimize curve_fit to determine Arrhenius
        parameters that result in best curve fit."""
        popt, pcov = curve_fit(self.get_eta_dim, self.T_exp,
        self.eta_mean, p0 = self.p0)
        self.A_arr = popt[0]
        self.T_a = popt[1]
        self.set_eta_dim()

    def get_S_r(self):
        """Returns sum of residuals squared for all data points."""
        S_r = sp.sum((self.eta_model - self.eta_exp)**2.)
        return S_r
        
