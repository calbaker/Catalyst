"""Contains class definition for catalyst."""

# Distribution libraries
import xlrd
import numpy as np
from scipy.optimize import curve_fit
import scipy.interpolate as interp

# Local libraries
import properties as prop
reload(prop)
import constants as const
reload(const)


class Catalyst(object):

    """Class for representing catalyst reactor modeled by multi term
    expansion"""

    CtoK = 273.15  # conversion from Celsius to Kelvin

    def __init__(self, **kwargs):
        """Sets values of constants"""
        self.P = 101.325  # Pressure of flow (kPa)

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

        self.lambda_array = self.lambda_and_Da[:, 0]

        if 'terms' in kwargs:
            self.terms = kwargs['terms']
            if self.terms > self.lambda_and_Da.shape[1] - 1:
                self.terms = self.lambda_and_Da.shape[1] - 1
                print "lambda are available for no more than 4 terms."
            self.lambda_and_Da = self.lambda_and_Da[:, : self.terms + 1]

        self.A_arr = 1.e7
        # Arrhenius coefficient (1/s ???)
        self.T_a = 7.206e3  # activation temperature (K)

        # Nanowire morphology
        self.porosity = 0.97  # porosity of nanowires
        self.tortuosity = self.porosity ** -1
        # tortuosity of nanowires
        self.Kn_length = 100e-9
        # Knudsen length (m) scale
        self.thickness = 5.e-6
        # Thickness of wash coat or height of porous media (m).  This
        # was h_{pore} in the pdf.

        # Channel geometry
        self.height = 0.0025
        # channel height (m)
        self.length = 76.2e-3 * 2.
        # channel length (m)
        self.width = 20e-3  # channel width (m)

        self.T_ambient = 300.
        # ambient temperature (K) at which flow rate is measured

        self.fuel = prop.ideal_gas(species='C3H8')
        self.air = prop.ideal_gas()

    def get_Y(self, x_, y_, **kwargs):

        """Sets non-dimensional Y at specified non-d (x, y) point.
        
        """
        
        if 'Pe' in kwargs:
            Pe = kwargs['Pe']
        else:
            Pe = self.get_Pe(???)

        if 'A_i' in kwargs:
            A_i = kwargs['A_i']
        else:
            A_i = self.get_A(self.T)

        if 'lambda_i' in kwargs:
            lambda_i = kwargs['lambda_i']
        else:
            lambda_i = self.get_lambda(self.T)

        Y = (
            (A_i * np.exp(-4. * lambda_i ** 2. / Pe * x_) *
            np.cos(lambda_i * y_)).sum()
            )

        return Y

    def get_A_i(self, *args, **kwargs):

        """Returns pre-exponential Arrhenius coefficient.

        Inputs: 

        Expects lambda_i or keyword argument T.  The default argument,
        lambda_i, can be obtained using get_lambda."""

        if 'T' in kwargs:
            T = kwargs['T']
            lambda_i = self.get_lambda(T)
        else:
            lambda_i = args[0]

        A_i = (
            2. * np.sin(lambda_i) / (lambda_i + np.sin(lambda_i) *
            np.sin(lambda_i))
            )

        return A_i

    def get_lambda(self, *args, **kwargs):

        """Uses spline fit to represent lambda as a function of Da.

        Inputs:
        
        Expects Da or keyword argument T.  The default argument, Da,
        can be obtained using get_Da.

        Values are handpicked from graph of lambda v Da.  Da is
        necessary argument.  Returns value of lambda at specified
        Da."""

        if 'T' in kwargs:
            T = kwargs['T']
            Da = np.float32(self.get_Da(T))
        else:
            Da = args[0]

        spline = []
        lambda_i = np.zeros(self.lambda_and_Da.shape[1] - 1)

        for i in range(0, self.lambda_and_Da.shape[1] - 1):
            spline.append(interp.splrep(self.lambda_array,
            self.lambda_and_Da[:, i]))
            lambda_i[i] = interp.splev(Da, spline[i])

        return lambda_i

    def get_Da(self, *args, **kwargs):

        """Returns Damkoehler number.

        Inputs:

        Expects D_C3H8_air, D_C3H8_air_eff, and thiele or keyword
        argument T. Defaults can be obtained with get_D_C3H8_air,
        get_D_C3H8_air_eff, and get_thiele."""

        if 'T' in kwargs:
            T = kwargs['T']
            T = T + self.CtoK
            D_C3H8_air = self.get_D_C3H8_air(T)
            D_C3H8_air_eff = self.get_D_C3H8_air_eff(T)
            thiele = self.get_thiele(T)

        elif len(args) != 2:
            print 'Not enough arguments were provided to get_Da'
            
        else:
            D_C3H8_air = args[0]
            D_C3H8_air_eff = args[1]
            thiels = args[2]

        Da = (
            0.5 * D_C3H8_air_eff / D_C3H8_air * self.height /
            self.thickness * np.sqrt(thiele) *
            np.tanh(np.sqrt(thiele))
           )

        return Da

    def get_thiele(self, *args, **kwargs):

        """Returns Thiele modulus.

        Inputs:

        Expects k_arr, D_C3H8_air_eff, """

        if 'T' in kwargs:
            T = kwargs['T']
            k_arr = (self.A_arr * np.exp(-self.T_a / T))
            D_C3H8_air_eff = self.get_D_C3H8_air_eff(T)
        else:
            k_arr = args[0]
            D_C3H8_air_eff = args[1]

        thiele = (k_arr * self.thickness ** 2 / D_C3H8_air_eff)

        return thiele

    def get_Pe(self, Vdot, T, **kwargs):

        """Returns Peclet number

        Inputs:

        Vdot : flow rate (m^3/s)
        T : temperature (K).
        
        D_C3H8_air can be given as a keyword argument to speed
        things up.  This can be returned by get_D_C3H8_air.

        """

        T = T + self.CtoK

        if D_C3H8_air in kwargs:
            D_C3H8_air = kwargs['D_C3H8_air']
        else:
            D_C3H8_air = self.get_D_C3H8_air(T)

        U = Vdot / (self.width * self.height) * (T / self.T_ambient)

        Pe = U * self.height / D_C3H8_air

        return Pe

    def get_mfp(self, *args, **kwargs):

        """Returns crude approximation of mfp (m) of propane in air

        Method from Bird, Stewart, Lightfoot Eq. 17.3-3.

        Input:

        Expects
        n : number density (#/m^3

        or keyword argument
        T : temperature (K)

        Output:

        mfp : mean free path (m) of air molecule"""

        if T in kwargs:
            T = kwargs['T']
            self.set_TempPres_dependents(T)
            n = self.air.n
        else:
            n = args[0]

        mfp = (
            (np.sqrt(2.) * np.pi * self.air.d ** 2. * n) ** -1.
            )

        return mfp

    def get_Kn(self, *args, **kwargs):

        """Returns Knudsen number for air.

        Inputs:
        
        Expects mean free path from get_mfp or optionally T as a
        keyword argument.  

        self.Kn_length must be set.
        
        Returns
        ___________
        Kn : Knudsen number"""

        if T in kwargs:
            T = kwargs['T']
            mfp = self.get_mfp(T)
        else:
            mfp = args[0]

        Kn = mfp / self.Kn_length

        return Kn

    def get_D_C3H8_air_eff(self, *args, **kwargs):

        """Returns effective diffusion coefficient in porous media.
        
        Inputs:
        
        Kn, D_C3H8_air, and D_C3H8_air_Kn from get_Kn, get_D_C3H8_air,
        and get_D_C3H8_air_Kn or T as keyword argument

        I need to put a refernce here for this scaling technique.  I'm
        pretty sure it is documented in the paper."""

        if T in kwargs:
            T = kwargs['T']
            Kn            = self.get_Kn(T)
            D_C3H8_air    = self.get_D_C3H8_air(T)
            D_C3H8_air_Kn = self.get_D_C3H8_air_Kn(T)
        else:
            Kn            = args[0]
            D_C3H8_air    = args[1]
            D_C3H8_air_Kn = args[2]

        if np.isscalar(Kn):
            if Kn <= 1.:
                D_C3H8_air_eff = (
                    self.porosity / self.tortuosity * D_C3H8_air
                    )
            else:
                D_C3H8_air_eff = (
                    2. * self.porosity / self.tortuosity * (D_C3H8_air
            * D_C3H8_air_Kn) / (D_C3H8_air + D_C3H8_air_Kn)
                    )

        else:
            if Kn.any() <= 1.:
                D_C3H8_air_eff = (
                    self.porosity / self.tortuosity * D_C3H8_air
                    )
            else:
                D_C3H8_air_eff = (
                    2. * self.porosity / self.tortuosity * (D_C3H8_air
            * D_C3H8_air_Kn) / (D_C3H8_air + D_C3H8_air_Kn)
                    )

        return D_C3H8_air_eff

    def get_D_C3H8_air_Kn(self, T):

        """Returns Knudsen diffusion coefficient for fuel/air."""

        D_C3H8_air = self.get_D_C3H8_air(T)
        Kn = self.get_Kn(T)

        D_C3H8_air_Kn = D_C3H8_air / Kn

        return D_C3H8_air_Kn

    def get_D_C3H8_air(self, T):

        """Returns binary diffusion coefficient for fuel/air.

        Method is from Bird, Stewart, Lightfoot Transport Phenomena
        2nd Ed. Equation 17.3-10"""

        self.set_TempPres_dependents(T)

        D_C3H8_air = (
            2. / 3. * np.sqrt(const.k_B * T / np.pi * 0.5 *
                                       (1. / self.air.m + 1. /
                                       self.fuel.m)) / (np.pi * (0.5 *
                                       (self.air.d +
                                       self.fuel.d)) ** 2.) /
                                       self.air.n
            )

        return D_C3H8_air

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

    def set_eta_ij(self):

        """Sets conversion efficiency over a range of Pe and Da."""

        self.Pe_ij = np.zeros(
            [self.Vdot_array.size, self.T_array.size]
            )
        self.Da_j = np.zeros(self.T_array.size)
        self.eta_ij = np.zeros(self.Pe_ij.shape)

        for i in np.arange(self.Vdot_array.size):
            for j in np.arange(self.T_array.size):
                Vdot = self.Vdot_array[i]
                T = self.T_array[j]

                self.eta_ij[i, j] = self.get_eta(Vdot, T)
                self.Da_j[j] = self.get_Da(T)
                self.Pe_ij[i, j] = self.get_Pe(Vdot, T)

    def get_eta(self, Vdot, T):

        """Returns conversion efficiency.

        Inputs:

        Vdot : flow rate (m^3/s)
        T : temperature (K).
        """

        try:
            self.x_
        except AttributeError:
            self.x_ = self.length / self.height

        A_i = self.get_A_i(T)
        lambda_i = self.get_lambda(T)
        Pe = self.get_Pe(Vdot, T)

        eta = (
            (A_i / lambda_i * np.sin(lambda_i) * (1. -
            np.exp(-lambda_i ** 2. / (4. * Pe) * self.x_))).sum()
            )

        return eta

    def import_data(self):

        """Imports data from excel sheet."""

        self.worksheet = xlrd.open_workbook(filename=self.source).sheet_by_index(0)
        # Import conversion data from worksheet and store as scipy arrays
        self.T_exp = np.array(
            self.worksheet.col_values(0, start_rowx=4, end_rowx=None)
            )
        self.HCout_raw = np.array(
            self.worksheet.col_values(4, start_rowx=4, end_rowx=None)
            )
        self.HCin_raw = np.array(
            self.worksheet.col_values(8, start_rowx=4, end_rowx=None)
            )
        self.eta_exp = (
            (self.HCin_raw - self.HCout_raw) / self.HCin_raw
            )
        self.T_array = np.linspace(self.T_exp[0], self.T_exp[-1], 50)

    def set_fit_params(self):

        """Uses scipy optimize curve_fit to determine Arrhenius
        parameters that result in best curve fit."""

        self.p0 = np.array([self.A_arr, self.T_a])
        # initial guess at A_arr and T_a

        self.popt, self.pcov = curve_fit(
            self.get_eta_dim, self.T_exp, self.eta_exp, p0 = self.p0
            )

        self.A_arr = self.popt[0]
        self.T_a = self.popt[1]

        self.set_eta_ij()

    def get_eta_dim(self, T, A_arr, T_a):

        """Returns species conversion efficiency, eta, as a function
        of required argument T. Used by set_params."""

        self.A_arr = A_arr
        self.T_a = T_a

        self.Pe_ij = self.get_Pe(self.Vdot, T)

        eta = self.get_eta(self.Vdot, T)

        return eta

    def get_S_r(self):

        """Returns sum of residuals squared for all data points."""

        S_r = np.sum((self.eta_model - self.eta_exp)**2.)

        return S_r
