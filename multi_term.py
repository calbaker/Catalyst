import numpy as np
import scipy as sp
import scipy.interpolate as interp

import properties as prop
import functions as func
import experimental_data as expdata
reload(expdata)

class Catalyst(expdata.ExpData):
    """Class for representing catalyst reactor modeled by multi term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
        expdata.ExpData.__init__(self)
        self.CtoK = 273.15 # conversion from Celsius to Kelvin
        self.P = 100. # Pressure of flow (kPa)

        self.lambda_and_Da = sp.array(
            [[0.001,0.0316,3.142,6.28,9.42],
             [0.002,0.0447,3.141,6.28,9.42],
             [0.003,0.0547,3.141,6.28,9.42], 
             [0.01,0.100,3.144,6.28,9.43],
             [0.02,0.141,3.15,6.28,9.43],
             [0.03,0.172,3.15,6.29,9.43], 
             [0.1,0.31,3.17,6.30,9.44],
             [0.2,0.43,3.20,6.31,9.45],
             [0.3,0.52,3.23,6.33,9.46],
             [0.4,0.59,3.26,6.35,9.46],
             [0.5,0.65,3.29,6.36,9.48],
             [1.0,0.86,3.43,6.44,9.53],
             [2.0,1.08,3.64,6.58,9.63],
             [5.0,1.31,4.03,6.91,9.89],
             [10.0,1.43,4.30,7.23,10.2],
             [5000.,1.57,4.71,7.85,11.0]] )
        # Graphically determined eigenvalues corresponding to Da

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
        self.Vdot_array = sp.linspace(100., 1000., 50) * 1.e-6 / 60. 
        # volume flow rate (m^3/s)
        self.T_array = sp.linspace(250., 450., 50) 
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
        spline1 = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,1]) 
        spline2 = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,2]) 
        spline3 = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,3]) 
        spline4 = interp.splrep(self.lambda_and_Da[:,0],
        self.lambda_and_Da[:,4]) 
        lambda1 = interp.splev(Da, spline1)
        lambda2 = interp.splev(Da, spline2)
        lambda3 = interp.splev(Da, spline3)
        lambda4 = interp.splev(Da, spline4)
        lambda_i = sp.array([lambda1,lambda2,lambda3,lambda4]) 
        return lambda_i

    def get_A(self,lambda_i):
        A = ( 2. * sp.sin(lambda_i) / (lambda_i + sp.sin(lambda_i) *
        sp.sin(lambda_i)) ) 
        return A

    def get_Y(self, x_, y_, Pe, lambda_i,A_i):
        """Sets float non-dimensional Y at any particular non-d (x,y)
        point""" 
        Y = ( sp.sum(A_i * np.exp(-4. * lambda_i**2. / Pe * x_) *
        np.cos(lambda_i * y_)) )   
        return Y

    def set_Yxy(self,Pe,Da):
        """Sets non-dimensional Y over a 2d array of non-dimensional
        x_ and y_"""
        lambda_i = self.get_lambda(Da)
        A_i = self.get_A(lambda_i)
        self.Yxy = np.zeros([np.size(self.x_array),
        np.size(self.y_array)])

        for i in sp.arange(sp.size(self.x_array)):
            for j in sp.arange(sp.size(self.y_array)):
                self.Yxy[i,j] = ( self.get_Y(self.x_array[i],
            self.y_array[j], Pe, lambda_i, A_i) )
    
    def get_eta(self, Da):
        """Returns species conversion efficiency, eta, as a function
        of required arguments Da and Pe"""
        lambda_i = self.get_lambda(Da)
        A_i = self.get_A(lambda_i)
        eta = ( (sp.sum(A_i / lambda_i * sp.sin(lambda_i)) - sp.sum(A_i
        / lambda_i * sp.exp(-lambda_i**2 / (4. * self.Pe_ij) *
        self.length_) * sp.sin(lambda_i))) )
        return eta
