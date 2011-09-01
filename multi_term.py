import numpy as np
import scipy as sp
import scipy.interpolate as interp

import properties as prop

class Catalyst():
    """Class for representing catalyst reactor modeled by 5 term
    expansion""" 

    def __init__(self):
        """Sets values of constants"""
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
             [5.0,1.31,4.03,6.91,9.89]] )
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
        self.air = prop.ideal_gas()

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
    
    def get_eta(self, Pe, Da):
        """Returns species conversion efficiency, eta, as a function
        of required arguments Da and Pe"""
        lambda_i = self.get_lambda(Da)
        A_i = self.get_A(lambda_i)
        eta = ( 1. - sp.sum(A_i / lambda_i * sp.exp(-lambda_i**2 / (4. *
        Pe) * self.length_) * sp.sin(lambda_i))  )
        return eta
        
    def set_eta(self):
        """Sets conversion efficiency over a range of Pe and Da."""
        self.set_Da()
        self.set_Pe()
        self.eta = sp.zeros([sp.size(self.Pe_array,0),
        sp.size(self.Da_array)])
        for i in sp.arange(sp.size(self.Pe_array,0)):
            for j in sp.arange(sp.size(self.Da_array)):
                self.eta[i,j] = self.get_eta(self.Pe_array[i,j],
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
                
    def set_Pe(self):
        """Sets Peclet number for a temperature and flow rate range of
        interest."""
        self.Pe_array = (
        sp.empty([sp.size(self.Vdot_array),sp.size(self.T_array)]) )

        for i in range(sp.size(self.Vdot_array)):
            for j in range(sp.size(self.T_array)):
                self.Pe_array[i,j] = (
            self.get_Pe(self.Vdot_array[i],self.T_array[j]) )
        
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
        ) # THIS FORMULA IS NOT CORRECT FOR MULTI TERM!!!!!
          # ****************************** ###########################
          # ?????????????????? 
        return Da
        
    def set_Da(self):
        """Sets Dahmkohler number for temperature range of
        interest."""
        self.Da_array = sp.empty(sp.size(self.T_array))

        for i in range(sp.size(self.T_array)):
            self.Da_array[i] = (
            self.get_Da(self.T_array[i],self.A_arr,self.T_a) ) 
