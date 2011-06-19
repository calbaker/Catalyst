import numpy as np
import scipy as sp

import properties as prop

class One_Term_Catalyst():
    """Class for representing catalyst reactor modeled by 1 term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
        self.P = 100. # Pressure of flow (kPa)
        self.Da = 1. # Damkoehler number
        self.Pe = 500. # Peclet number
        self.Da_fix = ( sp.array([0.1, 0.5, 1., 2., 5., 10., 15., 20.,
        30., 40., 50.]) ) # Graphically determined Da
        self.lambda_1 = ( sp.array([0.31, 0.65, 0.86, 1.08, 1.31,
        1.43, 1.47, 1.50, 1.52, 1.53, 1.54]) )
        # Graphically determined eigenvalues corresponding to Da
        self.ORDER = sp.size(self.Da_fix) - 1 - 6
        # order of polynomial fit
        self.Da_array = sp.arange(0.1, 10., 0.1)
        # Range of Da for plotting conversion efficiency
        self.Pe_array = sp.arange(100., 1000., 25.)
        # Range of Pe for plotting conversion efficiency
        self.length_ = 100.
        # dimensionless channel length
        self.height = 0.002
        # channel height (m)
        self.length = 76.2e-3 * 2.
        # channel length (m)
        self.thickness = 5.e-6
        # Thickness of wash coat or height of porous media (m).  This
        # was h_{pore} in the pdf.
        self.width = 20e-3 # channel width (m)
        self.Vdot = sp.arange(100., 1000., 10) * 1.e-6 / 60. 
        # volume flow rate (m^3/s)
        self.T = sp.arange(200., 600., 10.)
        # temperature of flow (K)
        self.A_arr = 2.e2
        # Arrhenius coefficient (not sure what the units are)
        self.T_a = 500. # activation temperature (K)
        self.porosity = 0.9

    fuel = prop.ideal_gas(species='C3H8')
    air = prop.ideal_gas()

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
        
    def set_diffusivity(self):
        """Sets thermal diffusivity based on BSL Transport Phenomena
        Eq. 17.3-10"""
        self.air.T = self.T
        self.air.P = self.P
        self.air.set_TempPres_dependents()
        self.fuel.T = self.T
        self.fuel.P = self.P
        self.fuel.set_TempPres_dependents()
        self.D_C3H8_air = ( 2./3. * sp.sqrt(self.air.k_B * self.T /
        sp.pi * 0.5 * (1. / self.air.m + 1. / self.fuel.m)) / (sp.pi *
        (0.5 * (self.air.d + self.fuel.d))**2.) / self.air.n )
        # Bindary diffusion coefficient from Bird, Stewart, Lightfoot
        # Transport Phenomena 2nd Ed. Equation 17.3-10

    def set_Pe(self):
        """Finds Peclet number as a function of flow rate (m^3/s),
        temperature (K), and geometry"""
        self.set_diffusivity()
        self.Pe_ij = sp.zeros([sp.size(self.Vdot), sp.size(self.T)])
        self.U = self.Vdot / (self.width * self.height)
        # flow velocity (m/s)
        for i in sp.arange(sp.size(self.Vdot)):
            for j in sp.arange(sp.size(self.T)):
                self.Pe_ij[i,j] = self.U[i] * self.height / self.D_C3H8_air[j]
                
    def set_Da(self):
        """Finds Damkoehler number as a function of temperature (K),
        porosity, catalyst loading and a whole slew of other
        things."""
        self.set_diffusivity()
        self.mfp = ( (sp.sqrt(2.) * sp.pi * self.air.d**2. *
        self.air.n)**-1. )
        # Crude approximation of mean free path (m) of propane in air from
        # Bird, Stewart, Lightfoot Eq. 17.3-3. Needs improvement.
        self.k_arr = self.A_arr * sp.exp(-self.T_a / self.T)
        self.D_C3H8_air_eff = ( self.D_C3H8_air * self.porosity ) 
        self.Da_pore_j = sp.zeros(sp.size(self.T))
        self.Da_j = sp.zeros(sp.size(self.T))
        for j in sp.arange(sp.size(self.T)):
            self.Da_pore_j = ( self.k_arr[j] * self.thickness**2 /
        self.D_C3H8_air_eff[j] )   
            self.Da_j[j] = 37.
        
