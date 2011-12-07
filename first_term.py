import numpy as np

import scipy.interpolate as interp

import properties as prop
import functions as func
from experimental_data import ExpData

class One_Term_Catalyst(ExpData):
    """Class for representing catalyst reactor modeled by 1 term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
        ExpData.__init__(self)
        self.CtoK = 273.15 # conversion from Celsius to Kelvin
        self.P = 100. # Pressure of flow (kPa)
        self.Da = 1. # Damkoehler number
        self.Pe = 500. # Peclet number

        self.lambda_and_Da = np.array(
            [[0.001,0.0316], [0.002,0.0447], [0.003,0.0547], 
            [0.01,0.100], [0.02,0.141], [0.03,0.172], 
             [0.1,0.31], [0.2,0.43], [0.3,0.52], [0.4,0.59],
            [0.5,0.65],
             [1.0,0.86], [2.0,1.08], [5.0,1.31],
             [10.0,1.43], [15.0,1.47], [20.0,1.50], [30.0,1.52],
            [40.0,1.53], [50.0,1.54], [150., 1.56],
             [5000., 1.57]])    
        
        # Graphically determined eigenvalues corresponding to Da
        self.Da_array = np.arange(1., 20., 0.5)
        # Range of Da for plotting conversion efficiency
        self.Pe_array = np.arange(1., 100., 2.)
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
        self.Vdot_array = np.linspace(100., 1000., 50) * 1.e-6 / 60. 
        # volume flow rate (m^3/s)
        self.T_array = np.linspace(250., 450., 50) 
        # temperature of flow (C)
        self.T_ambient = 300.
        # ambient temperature (K) at which flow rate is measured
        self.A_arr = 1.e7
        # Arrhenius coefficient (1/s ???)
        self.T_a = 6.93e3 # activation temperature (K)
        self.porosity = 0.97
        self.fuel = prop.ideal_gas(species='C3H8')
        self.air = prop.ideal_gas()
        
        self.set_eta = types.MethodType(func.set_eta, self)
        self.get_diffusivity = types.MethodType(func.get_diffusivity,
        self) 
        self.get_Pe = types.MethodType(func.get_Pe, self)
        self.set_Pe = types.MethodType(func.set_Pe, self)
        self.get_Da = types.MethodType(func.get_Da, self)
        self.set_Da = types.MethodType(func.set_Da, self)
    
    def get_lambda(self, Da):
        """Uses fit algorithm to represent lambda as a function of Da
        with handpicked values.
        Da is necessary argument.  Returns value of lambda at
        specified Da.""" 
        Da = np.float32(Da)
        spline_params = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,1]) 
        lambda_fit = interp.splev(Da, spline_params)
        return lambda_fit

    def get_Y(self, x_, y_, Pe, Da):
        """Sets float non-dimensional Y at any particular non-d (x,y)
        point""" 
        lambda1 = self.get_lambda(Da)
        Y = ( lambda1 / lambda1 * np.exp(-lambda1**2. / (4. * Pe) *
        x_) * np.cos(lambda1 * y_) )     
        return Y

    def set_Yxy(self,Pe,Da):
        """Sets non-dimensional Y over a 2d array of non-dimensional
        x_ and y_"""
        self.Yxy = np.zeros([np.size(self.x_array),
        np.size(self.y_array)])

        for i in np.arange(np.size(self.x_array)):
            for j in np.arange(np.size(self.y_array)):
                self.Yxy[i,j] = ( self.get_Y(self.x_array[i],
            self.y_array[j], Pe, Da) )
    
    def get_eta(self, Da):
        """Returns species conversion efficiency, eta, as a function
        of required argument Da."""
        Lambda = self.get_lambda(Da)
        eta = ( 1. - np.exp(-Lambda**2. / (4. * self.Pe_ij) *
        self.length_) )  
        return eta
