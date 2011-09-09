"""Module containing funcitons that are common to both first term and
multi-term catalyst models."""

import scipy as sp

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
