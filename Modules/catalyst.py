"""Contains class definition for catalyst."""

# Distribution libraries
import numpy as np
import scipy.interpolate as interp

# Local libraries
import properties as prop
reload(prop)
import constants as const
reload(const)

class Catalyst(object):
    """Class for representing catalyst reactor modeled by multi term
    expansion""" 

    CtoK = 273.15 # conversion from Celsius to Kelvin

    def __init__(self, **kwargs):
        """Sets values of constants"""
        self.P = 100. # Pressure of flow (kPa)

        self.lambda_and_Da = np.array(
            [[0.001, 0.0316, 3.142, 6.28, 9.42],
             [0.002, 0.0447, 3.141, 6.28, 9.42],
             [0.003, 0.0547, 3.141, 6.28, 9.42], 
             [0.01,  0.100,  3.144, 6.28, 9.43],
             [0.02,  0.141,  3.15,  6.28, 9.43], 
             [0.03,  0.172,  3.15,  6.29, 9.43],  
             [0.1,   0.31,   3.17,  6.30, 9.44], 
             [0.2,   0.43,   3.20,  6.31, 9.45], 
             [0.3,   0.52,   3.23,  6.33, 9.46], 
             [0.4,   0.59,   3.26,  6.35, 9.46], 
             [0.5,   0.65,   3.29,  6.36, 9.48], 
             [1.0,   0.86,   3.43,  6.44, 9.53], 
             [2.0,   1.08,   3.64,  6.58, 9.63], 
             [5.0,   1.31,   4.03,  6.91, 9.89], 
             [10.0,  1.43,   4.30,  7.23, 10.2], 
             [5000., 1.57,   4.71,  7.85, 11.0]])
        # Graphically determined eigenvalues corresponding to Da.
        # First column is Da, second column is lamba_0, third column
        # is lambda_1, and so on...

        self.lambda_array = self.lambda_and_Da[:,0]

        if 'terms' in kwargs:
            self.terms = kwargs['terms']
            if self.terms > 4:
                self.terms = 4
                print "lambda are available for no more than 4 terms."
            self.lambda_and_Da = self.lambda_and_Da[:, : self.terms + 1]

        self.A_arr = 1.e7
        # Arrhenius coefficient (1/s ???)
        self.T_a = 7.206e3 # activation temperature (K)
        self.porosity = 0.97 
        self.tortuosity = self.porosity**-1 

        self.Kn_length = 100e-9
        # Knudsen length (m) scale
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

        self.fuel = prop.ideal_gas(species='C3H8')
        self.air = prop.ideal_gas()
        
    def get_Y(self, x_, y_, Pe, lambda_i,A_i):

        """Sets non-dimensional Y at any particular non-d (x,y) point""" 
        Y = ( np.sum(A_i * np.exp(-4. * lambda_i**2. / Pe * x_) *
        np.cos(lambda_i * y_)) )   
        return Y

    def get_A(self, lambda_i):

        """Returns pre-exponential Arrhenius coefficient.

        Input:
        lambda_i : array of eigen values"""

        A = (2. * np.sin(lambda_i) / (lambda_i + np.sin(lambda_i) *
        np.sin(lambda_i))).sum() 

        return A

    def get_lambda(self, Da):

        """Uses spline fit to represent lambda as a function of Da.

        Values are handpicked from graph of lambda v Da.  Da is
        necessary argument.  Returns value of lambda at specified
        Da.""" 

        Da = np.float32(Da)

        self.spline = []
        self.lambda_i = []

        for i in range(1, self.lambda_and_Da.shape[1] - 1):
            self.spline.append(interp.splrep(self.lambda_array,
            self.lambda_and_Da[:,i])) 
            self.lambda_i[i]= interp.splev(Da, self.spline[i])

        return lambda_i

    def get_Pe(self, Vdot, T):

        """Returns Peclet number for a particular flow rate (m^3/s),
        temperature (K), and geometry"""

        T = T + self.CtoK
        D_C3H8_air = self.get_diffusivity(T, self.P)
        U = (Vdot / (self.width * self.height) * (T / self.T_ambient)) 
        Pe = U * self.height / D_C3H8_air

        return Pe

    def get_mfp(self, n):

        """Returns crude approximation of mfp (m) of propane in air 

        Method from Bird, Stewart, Lightfoot Eq. 17.3-3.  

        Input:

        n : number density of air (# / m^3)
        
        Output: 

        mfp : mean free path (m) of air molecule"""

        mfp = ( (np.sqrt(2.) * np.pi * self.air.d**2. * n)**-1. )   

        return mfp

    def get_Kn(self, n):

        """Returns Knudsen number for air. self.Kn_length must be set
        first.  
        
        Returns
        ___________
        Kn : Knudsen number"""

        mfp = self.get_mfp(n)

        self.Kn = mfp / self.Kn_length

        return self.Kn

    def get_diffusivity(self, T, P):
        """Returns binary diffusion coefficient from Bird, Stewart,
        Lightfoot Transport Phenomena 2nd Ed. Equation 17.3-10"""
        self.air.T = T
        self.air.P = P
        self.air.set_TempPres_dependents()
        self.fuel.T = T
        self.fuel.P = P
        self.fuel.set_TempPres_dependents()

        D_C3H8_air = (2./3. * np.sqrt(const.k_B * T / np.pi * 0.5 *
                                       (1. / self.air.m + 1. /
                                       self.fuel.m)) / (np.pi * (0.5 *
                                       (self.air.d +
                                       self.fuel.d))**2.) /
                                       self.air.n)    
        return D_C3H8_air 

