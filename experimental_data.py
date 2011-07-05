import scipy as sp

import first_term as ft

class Data(ft.One_Term_Catalyst):
    """Class for keeping track of experimental data"""

    def __init__(self):
        """Sets constants and initializes parent class."""
        self.T_ambient = 300. # ambient tempearture (K)
        self.CtoK = 273.15 # conversion from Celsisus to Kelvin
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
        self.HCout[i,j]) / self.HCin[i,j] / self.HCin.shape[1] ) 
            self.eta_mean[i] = self.eta_raw[i,:].sum()
            self.errorbar[i] = 1.96 * self.eta_raw[i,:].std() 

    def get_S_r(self):
        """Returns sum of residuals squared for all data points."""
        S_r = sp.sum((self.eta_model - self.eta_exp)**2.)
        return S_r
        
