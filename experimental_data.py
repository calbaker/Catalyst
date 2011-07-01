import scipy as sp

import first_term as ft

class Data(ft.One_Term_Catalyst):
    """Class for keeping track of experimental data"""

    def __init__(self):
        self.T_ambient = 300. # ambient tempearture (K)
        self.CtoK = 273.15 # conversion from Celsisus to Kelvin
        ft.One_Term_Catalyst.__init__(self)

    def set_eta(self):
        """Sets conversion efficiency based on inlet and oulet HC
    concentration from experiment and model for a range of
    temperatures. Vdot and T_array must be set for this to work.""" 
        self.eta_exp = sp.zeros(sp.size(self.T_array))
        self.eta_exp = (self.HCin - self.HCout) / self.HCin
        self.set_eta_dim()
        self.eta_model = self.eta_dim

    def get_R(self):
        """Returns sum of residuals squared for all data points."""
        
