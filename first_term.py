import numpy as np
import scipy as sp
import scipy.interpolate as interp
from scipy.optimize import curve_fit

import properties as prop

class One_Term_Catalyst():
    """Class for representing catalyst reactor modeled by 1 term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
        self.epsilon = 1. # Used for perturbation
        self.CtoK = 273.15 # conversion from Celsius to Kelvin
        self.P = 100. # Pressure of flow (kPa)
        self.Da = 1. # Damkoehler number
        self.Pe = 500. # Peclet number

        self.lambda_and_Da = sp.array(
            [[0.001,0.0316], [0.002,0.0447], [0.003,0.0547], 
            [0.01,0.100], [0.02,0.141], [0.03,0.172], 
             [0.1,0.31], [0.2,0.43], [0.3,0.52], [0.4,0.59],
            [0.5,0.65],
             [1.0,0.86], [2.0,1.08], [5.0,1.31],
             [10.0,1.43], [15.0,1.47], [20.0,1.50], [30.0,1.52],
            [40.0,1.53], [50.0,1.54]])    
        
        # Graphically determined eigenvalues corresponding to Da
        self.Da_array = sp.arange(1., 20., 0.5)
        # Range of Da for plotting conversion efficiency
        self.Pe_array = sp.arange(1., 100., 2.)
        # Range of Pe for plotting conversion efficiency
        self.length_ = 100.
        # dimensionless channel length
        self.height = 0.003
        # channel height (m)
        self.length = 76.2e-3 * 2.
        # channel length (m)
        self.thickness = 5.e-6
        # Thickness of wash coat or height of porous media (m).  This
        # was h_{pore} in the pdf.
        self.width = 20e-3 # channel width (m)
        self.Vdot_array = sp.arange(100., 1000., 10) * 1.e-6 / 60. 
        # volume flow rate (m^3/s)
        self.T_array = sp.arange(200., 600., 10.) 
        # temperature of flow (C)
        self.T_ambient = 300.
        # ambient temperature (K) at which flow rate is measured
        self.A_arr = 15.e9
        # Arrhenius coefficient (1/s ???)
        self.T_a = 14.e3 # activation temperature (K)
        self.porosity = 0.9

    fuel = prop.ideal_gas(species='C3H8')
    air = prop.ideal_gas()

    def get_lambda(self, Da):
        """Uses fit algorithm to represent lambda as a function of Da
        with handpicked values.
        Da is necessary argument.  Returns value of lambda at
        specified Da.""" 
        Da = Da.astype('float32')
        spline_params = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,1]) 
        lambda_fit = interp.splev(Da, spline_params)
        return lambda_fit

    def get_Y_(self, x_, y_):
        """Sets float non-dimensional Y at any particular non-d (x,y)
        point""" 
        lambda1 = self.get_lambda(self.Da)
        Y_ = ( lambda1 / self.lambda1 * sp.exp(-self.lambda1**2. /
        (4. * self.Pe ) * self.x_) * sp.cos(self.lambda1 * self.y_) )   
        return Y_

    def set_Yxy_(self):
        """Sets non-dimensional Y over a 2d array of non-dimensional
        x_ and y_"""
        self.Yxy_ = np.zeros([np.size(self.x_array),
        np.size(self.y_array)])

        for i in sp.arange(sp.size(self.x_array)):
            for j in sp.arange(sp.size(self.y_array)):
                self.Yxy_[i,j] = self.get_Y_(x_array[i], y_array[j]) 
    
    def get_eta(self, Pe, Da):
        """Returns species conversion efficiency, eta, as a function
        of required arguments Da and Pe"""
        Lambda = self.get_lambda(Da)
        eta = ( 1. - sp.exp(-Lambda**2. / (4. * Pe) * self.length_) )
        return eta
        
    def set_eta_dimless(self):
        """Sets conversion efficiency over a range of Pe and Da."""
        self.eta_dimless = sp.zeros([sp.size(self.Pe_array),
        sp.size(self.Da_array)])
        self.lambda_j = sp.zeros(sp.size(self.Da_array))
        for i in sp.arange(sp.size(self.Pe_array)):
            for j in sp.arange(sp.size(self.Da_array)):
                self.eta_dimless[i,j] = self.get_eta(self.Pe_array[i],
        self.Da_array[j]) 
        
    def get_diffusivity(self, T, P):
        """Sets thermal diffusivity based on BSL Transport Phenomena
        Eq. 17.3-10"""
        self.air.T = T
        self.air.P = P
        self.air.set_TempPres_dependents()
        self.fuel.T = T
        self.fuel.P = P
        self.fuel.set_TempPres_dependents()
        D_C3H8_air = ( 2./3. * sp.sqrt(self.air.k_B * T /
        sp.pi * 0.5 * (1. / self.air.m + 1. / self.fuel.m)) / (sp.pi *
        (0.5 * (self.air.d + self.fuel.d))**2.) / self.air.n )
        # Bindary diffusion coefficient from Bird, Stewart, Lightfoot
        # Transport Phenomena 2nd Ed. Equation 17.3-10
        return D_C3H8_air 

    def get_Pe(self, Vdot, T):
        """Returns Peclet number for a particular flow rate (m^3/s),
        temperature (K), and geometry"""
        T = T + self.CtoK
        D_C3H8_air = self.get_diffusivity(T, self.P)
        U = ( Vdot / (self.width * self.height) * (T / self.T_ambient)
        ) 
        Pe = U * self.height / D_C3H8_air
        return Pe
                
    def get_Da(self, T, A_arr, T_a):
        """Returns Damkoehler for a particular temperature (K),
        porosity, catalyst loading and a whole slew of other things."""
        T = T + self.CtoK
        k_arr = ( A_arr * sp.exp(-T_a / T) )
        D_C3H8_air = self.get_diffusivity(T, self.P)
        D_C3H8_air_eff = ( D_C3H8_air * self.porosity ) 
        mfp = ( (sp.sqrt(2.) * sp.pi * self.air.d**2. *
        self.air.n)**-1. )  
        # Crude approximation of mean free path (m) of propane in air from
        # Bird, Stewart, Lightfoot Eq. 17.3-3. Needs improvement.
        Da_pore = ( k_arr * self.thickness**2 / D_C3H8_air_eff )   
        Da = ( D_C3H8_air_eff / D_C3H8_air * self.height /
        self.thickness * sp.sqrt(Da_pore) * sp.tanh(sp.sqrt(Da_pore))
        ) 
        return Da
        
    def get_eta_dim(self, T, A_arr, T_a):
        """Returns conversion efficiency for a particular flow rate and
        temperature."""
        Da = self.get_Da(T, A_arr, T_a)
        Pe = self.get_Pe(self.Vdot, T)
        Lambda = self.get_lambda(Da) 
        eta_dim = ( 1. - sp.exp(-Lambda**2. / (4. * Pe) *
        self.length_) )
        return eta_dim

    def set_eta_dim(self):
        """Sets conversion efficiency over a range of flow rate and
        temperature."""
        self.eta_dim = sp.zeros([sp.size(self.Vdot_array),
        sp.size(self.T_array)])
        for i in sp.arange(sp.size(self.Vdot_array)):
            for j in sp.arange(sp.size(self.T_array)):
                self.Vdot = self.Vdot_array[i]
                self.eta_dim[i,j] = self.get_eta_dim(self.T_array[j],
        self.A_arr, self.T_a)
