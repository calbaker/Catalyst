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
    temperatures. Vdot and T_array must be set for this to work.""" 
        self.eta_exp = sp.zeros(self.HCin.shape)
        for i in sp.size(self.HCin,0):
            for j in sp.size(self.HCin,1):
                self.eta_exp[i,j] = ( (self.HCin[i,j] -
        self.HCout[i,j]) / self.HCin[i,j] )

    def get_S_r(self):
        """Returns sum of residuals squared for all data points."""
        S_r = sp.sum((self.eta_model - self.eta_exp)**2.)
        return S_r
        
