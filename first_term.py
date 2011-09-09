import numpy as np
import scipy as sp
import scipy.interpolate as interp

import properties as prop
import functions as func

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
            [40.0,1.53], [50.0,1.54], [150., 1.56]])    
        
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
        self.T_array = sp.arange(350., 600., 5.) 
        # temperature of flow (C)
        self.T_ambient = 300.
        # ambient temperature (K) at which flow rate is measured
        self.A_arr = 42.2e9
        # Arrhenius coefficient (1/s ???)
        self.T_a = 12.2e3 # activation temperature (K)
        self.porosity = 0.9
        self.fuel = prop.ideal_gas(species='C3H8')

    air = prop.ideal_gas()
    set_eta = func.set_eta
    get_diffusivity = func.get_diffusivity
    get_Pe = func.get_Pe
    set_Pe = func.set_Pe
    get_Da = func.get_Da
    set_Da = func.set_Da
    
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
        Y = ( lambda1 / lambda1 * sp.exp(-lambda1**2. / (4. * Pe) *
        x_) * sp.cos(lambda1 * y_) )     
        return Y

    def set_Yxy(self,Pe,Da):
        """Sets non-dimensional Y over a 2d array of non-dimensional
        x_ and y_"""
        self.Yxy = np.zeros([np.size(self.x_array),
        np.size(self.y_array)])

        for i in sp.arange(sp.size(self.x_array)):
            for j in sp.arange(sp.size(self.y_array)):
                self.Yxy[i,j] = ( self.get_Y(self.x_array[i],
            self.y_array[j], Pe, Da) )
    
    def get_eta(self, Pe, Da):
        """Returns species conversion efficiency, eta, as a function
        of required arguments Da and Pe"""
        Lambda = self.get_lambda(Da)
        eta = ( 1. - sp.exp(-Lambda**2. / (4. * Pe) * self.length_) )
        return eta
