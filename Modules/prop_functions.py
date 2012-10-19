import numpy as np
import constants as const
reload(const)

def get_Da(self, *args):

    """Returns Damkoehler number.

    Inputs:

    T: temperature (K)

    of if none:
    self.T is used
    """

    if len(args) == 1:
        T = args[0]
    
    else:
        T = self.T

    thiele = self.get_thiele(T)

    self.Da = (
        0.5 * self.D_C3H8_air_eff / self.D_C3H8_air * self.height /
        self.thickness * np.sqrt(thiele) * np.tanh(np.sqrt(thiele)) 
       )

    return self.Da

def get_thiele(self, T):

    """Returns Thiele modulus.

    Inputs:

    T: temperature (K)"""

    k_arr = (self.A_arr * np.exp(-self.T_a / T))
    D_C3H8_air_eff = self.get_D_C3H8_air_eff(T)

    self.thiele = (k_arr * self.thickness ** 2 / D_C3H8_air_eff)

    return self.thiele

def get_k(self, T):

    """Returns Thiele modulus.

    Inputs:

    T: temperature (K)"""

    self.k_arr = self.A_arr * np.exp(-self.T_a / T)

    return self.k_arr

def get_Pe(self, *args):

    """Returns Peclet number

    Inputs:

    Vdot : flow rate (m^3/s)
    T : temperature (K).

    if if none:
    Vdot = self.Vdot
    T = self.T

    """

    if len(args) == 2:
        Vdot = args[0]
        T = args[1]

    else:
        Vdot = self.Vdot
        T = self.T

    D_C3H8_air = self.get_D_C3H8_air(T)

    self.U = Vdot / (self.width * self.height) * (T / self.T_ambient)

    self.Pe = self.U * self.height / D_C3H8_air

    return self.Pe

def set_TempPres_dependents(self, T):

    """Performance this function on both fuel and air.

    Input:
    T : temperature (K)

    Requires that self.P is set."""

    self.air.T = T
    self.air.P = self.P
    self.air.set_TempPres_dependents()
    self.fuel.T = T
    self.fuel.P = self.P
    self.fuel.set_TempPres_dependents()

def get_mfp(self, T):

    """Returns crude approximation of mfp (m) of propane in air

    Method from Bird, Stewart, Lightfoot Eq. 17.3-3.

    Input:

    T : temperature (K)

    Output:

    mfp : mean free path (m) of air molecule"""

    self.air.T = T
    self.air.set_TempPres_dependents()

    self.mfp = (
        (np.sqrt(2.) * np.pi * self.air.d ** 2. * self.air.n) ** -1.
        )

    return self.mfp

def get_Kn(self, T):

    """Returns Knudsen number for air.

    Inputs:

    T: temperature (K)

    self.Kn_length must be set.

    Returns
    ___________
    Kn : Knudsen number"""

    mfp = self.get_mfp(T)

    self.Kn = mfp / self.Kn_length

    return self.Kn

def get_D_C3H8_air_eff(self, T):

    """Returns effective diffusion coefficient in porous media.

    Inputs:

    T: temperature (K)

    I need to put a refernce here for this scaling technique.  I'm
    pretty sure it is documented in the paper."""

    Kn = self.get_Kn(T)
    D_C3H8_air_Kn = self.get_D_C3H8_air_Kn(T)

    if np.isscalar(Kn):
        if Kn <= 1.:
            D_C3H8_air_eff = (
                self.porosity / self.tortuosity * self.D_C3H8_air
                )
        else:
            D_C3H8_air_eff = (
                2. * self.porosity / self.tortuosity *
        (self.D_C3H8_air * D_C3H8_air_Kn) / (self.D_C3H8_air +
        D_C3H8_air_Kn)
                )

    else:
        if Kn.any() <= 1.:
            D_C3H8_air_eff = (
                self.porosity / self.tortuosity * self.D_C3H8_air
                )
        else:
            D_C3H8_air_eff = (
                2. * self.porosity / self.tortuosity *
        (self.D_C3H8_air * D_C3H8_air_Kn) / (self.D_C3H8_air +
        D_C3H8_air_Kn)
                )

    self.D_C3H8_air_eff = D_C3H8_air_eff

    return D_C3H8_air_eff

def get_D_C3H8_air_Kn(self, T):

    """Returns Knudsen diffusion coefficient for fuel/air.

    T: temperature (K)
    """

    Kn = self.get_Kn(T)
    D_C3H8_air = self.get_D_C3H8_air(T)

    self.D_C3H8_air_Kn = D_C3H8_air / Kn

    return self.D_C3H8_air_Kn

def get_D_C3H8_air(self, T):

    """Returns binary diffusion coefficient for fuel/air.

    Method is from Bird, Stewart, Lightfoot Transport Phenomena
    2nd Ed. Equation 17.3-10

    Inputs:
    T : temperature

    Output:

    mfp : mean free path (m) of air molecule"""

    self.set_TempPres_dependents(T)

    self.D_C3H8_air = (
        2. / 3. * np.sqrt(const.k_B * T / np.pi * 0.5 * (1. /
        self.air.m + 1. / self.fuel.m)) / (np.pi * (0.5 *
        (self.air.d + self.fuel.d)) ** 2.) / self.air.n
        )

    return self.D_C3H8_air

