"""Contains class definition for catalyst."""

# Distribution libraries
import xlrd
import numpy as np
from scipy.optimize import curve_fit
import scipy.interpolate as interp
from scipy.integrate import odeint

# Local libraries
import properties as prop
reload(prop)
import constants as const
reload(const)


class Catalyst(object):

    """Class for representing catalyst reactor.

    Reactor can modeled by 1 to 4 term Fourier expansion.

    A word on units:
    Pressure is always in kPa unless otherwise specified
    Temperature ditto K ditto
    Lengths ditto m ditto"""

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
             [5000., 1.57,   4.71,  7.85, 11.0]] )
        # Graphically determined eigenvalues corresponding to Da.
        # First column is Da, second column is lamba_0, third column
        # is lambda_1, and so on...

        if 'terms' in kwargs:
            self.terms = kwargs['terms']
            if self.terms > self.lambda_and_Da.shape[1] - 1:
                self.terms = self.lambda_and_Da.shape[1] - 1
                print "lambda are available for no more than 4 terms."
            self.lambda_and_Da = (
                self.lambda_and_Da[:, : self.terms + 1]
                )
        else:
            self.terms = self.lambda_and_Da.shape[1] - 1
        self.init_lambda_splines()

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

        self.x_ = self.length / self.height
        # dimensionless x.  this will need to be reevaluated if length
        # or height is changed.

        self.x_nodes = 100
        # Number of streamwise nodes for which Y is returned in
        # numerical model.  

        self.y_ = 1.

        self.y_nodes = 50
        # Number of transverse nodes for which Y is returned in
        # numerical model.

        self.T_ambient = 300. + 273.15
        # ambient temperature (K) at which flow rate is measured

        self.fuel = prop.ideal_gas(species='C3H8')
        self.air = prop.ideal_gas()
        self.air.P = self.P
        self.fuel.P = self.P

    def init_lambda_splines(self):

        """Sets up spline fitting for get_lambda."""

        self.lambda_splines = []

        for i in range(0, self.lambda_and_Da.shape[1] - 1):
            self.lambda_splines.append(
                interp.splrep(self.lambda_and_Da[:, 0],
                              self.lambda_and_Da[:, i + 1])
                )
        self.lambda_splines = np.array(self.lambda_splines)

    def get_Y(self, x_, y_, **kwargs):

        """Sets non-dimensional Y at specified non-d (x, y) point.

        Inputs:

        x_ : streamwise coordinate scaled by channel height
        y_ : transverse coordinate scaled by channel height

        """

        # T and Vdot are generally going to be constants here so they
        # are not used as input arguments.  
        
        if 'Pe' in kwargs:
            Pe = kwargs['Pe']
            
        else:
            T = self.T  
            Vdot = self.Vdot
            Pe = self.get_Pe(Vdot, T)

        if 'Da' in kwargs:
            Da = kwargs['Da']
            A_i = self.get_A_i(Da=Da)
            lambda_i = self.lambda_i
        
        else:
            T = self.T  
            A_i = self.get_A_i(T)
            lambda_i = self.lambda_i

        self.Y = (
            (A_i * np.exp(-4. * lambda_i ** 2. / Pe * x_) *
            np.cos(lambda_i * y_)).sum()
            )

        return self.Y

    def get_lambda(self, *args, **kwargs):

        """Uses spline fit to represent lambda as a function of Da.

        Inputs:

        T : temperature (K)

        or keyword argument Da from get_Da
        """

        if 'Da' in kwargs:
            Da = kwargs['Da']

        else:
            T = args[0]
            Da = np.float32(self.get_Da(T))

        self.lambda_i = np.zeros(self.lambda_and_Da.shape[1] - 1)

        for i in range(len(self.lambda_splines)):
            self.lambda_i[i] = interp.splev(Da, self.lambda_splines[i])

        return self.lambda_i

    def get_A_i(self, *args, **kwargs):

        """Returns pre-exponential Arrhenius coefficient.

        Inputs:

        T: temperature (K)

        or keyword argument Da from get_Da
        """

        if len(args) == 1:
            T = args[0]
            lambda_i = self.get_lambda(T)

        elif 'Da' in kwargs:
            Da = kwargs['Da']
            lambda_i = self.get_lambda(Da=Da)

        self.A_i = (
            2. * np.sin(lambda_i) / (lambda_i + np.sin(lambda_i) *
            np.sin(lambda_i))
            )

        return self.A_i

    def get_Da(self, T):

        """Returns Damkoehler number.

        Inputs:

        T: temperature (K) 
        """

        thiele = self.get_thiele(T)

        self.Da = (
            0.5 * self.D_C3H8_air_eff / self.D_C3H8_air * self.height
            / self.thickness * np.sqrt(thiele) *
            np.tanh(np.sqrt(thiele))  
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

    def get_Pe(self, Vdot, T):

        """Returns Peclet number

        Inputs:

        Vdot : flow rate (m^3/s)
        T : temperature (K).

        """

        D_C3H8_air = self.get_D_C3H8_air(T)

        U = Vdot / (self.width * self.height) * (T / self.T_ambient)

        self.Pe = U * self.height / D_C3H8_air

        return self.Pe

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

        self.x_ = self.length / self.height

        try:
            self.Vdot_array
        except AttributeError:
            self.Vdot_array = np.array([self.Vdot])

        self.Pe_ij = np.zeros(
            [self.Vdot_array.size, self.T_array.size]
            )
        self.Da_j = np.zeros(self.T_array.size)
        self.eta_ij = np.zeros(self.Pe_ij.shape)

        for i in np.arange(self.Vdot_array.size):
            for j in np.arange(self.T_array.size):

                self.Vdot = self.Vdot_array[i]
                self.T = self.T_array[j]

                self.eta_ij[i, j] = self.get_eta(self.Vdot, self.T)
                self.Da_j[j] = self.Da
                self.Pe_ij[i, j] = self.Pe

    def get_eta(self, Vdot, T):

        """Returns conversion efficiency.

        Inputs:
        Vdot : flow rate (m^3/s)
        T : temperature (K).
        """

        A_i = self.get_A_i(T)
        Pe = self.get_Pe(Vdot, T)
            
        self.eta = (
            (A_i / self.lambda_i * np.sin(self.lambda_i) * (1. -
            np.exp(-self.lambda_i ** 2. / (4. * Pe) * self.x_))).sum()
            )

        return self.eta

    def get_eta_fit(self, T_exp, A_arr, T_a):
        
        """Returns eta with inputs that are used by curve_fit
        
        Inputs:
        T: temperature (K)

        used by curve_fit as fit parameters:
        A_arr : pre-exponential coefficient for Arrhenius kinetics
        T_a : activation temperature (K)

        """

        self.A_arr = A_arr
        self.T_a = T_a

        self.T_array = T_exp
        self.set_eta_ij()

        self.eta_ij = self.eta_ij.reshape(self.eta_ij.size)

        return self.eta_ij

    def set_fit_params(self):

        """Uses scipy optimize curve_fit to determine Arrhenius
        parameters that result in best curve fit."""

        self.p0 = np.array([self.A_arr, self.T_a])
        # initial guess at A_arr and T_a

        self.popt, self.pcov = curve_fit(
            self.get_eta_fit, self.T_exp, self.eta_exp, p0=self.p0 
            )

        self.A_arr = self.popt[0]
        self.T_a = self.popt[1]

        self.T_array = self.T_model

    def get_S_r(self):

        """Returns sum of residuals squared for all data points."""

        S_r = np.sum((self.eta_model - self.eta_exp) ** 2.)

        return S_r

    def import_data(self):

        """Imports data from excel sheet."""

        self.worksheet = (
            xlrd.open_workbook(filename=self.source).sheet_by_index(0)
            )
        # Import conversion data from worksheet and store as scipy arrays
        self.T_exp = np.array(
            self.worksheet.col_values(0, start_rowx=4, end_rowx=None)
            ) + 273.15
        self.HCout_raw = np.array(
            self.worksheet.col_values(4, start_rowx=4, end_rowx=None)
            )
        self.HCin_raw = np.array(
            self.worksheet.col_values(8, start_rowx=4, end_rowx=None)
            )
        self.eta_exp = (
            (self.HCin_raw - self.HCout_raw) / self.HCin_raw
            )
        self.T_model = np.linspace(
            self.T_exp[0] - 50, self.T_exp[-1] + 50, 50
            )
        self.T_array = self.T_model

    def solve_numeric(self):
        
        """Solves for species and conversion numerically."""

        Y0 = np.zeros(self.y_nodes)
        self.x_array = np.linspace(0, self.x_, self.x_nodes)
        self.y_array = np.linspace(0, self.y_, self.y_nodes)
        self.delta_x = self.length / self.x_nodes
        self.delta_y = self.height / self.y_nodes
        
        self.Yxy_num = odeint(self.get_Yprime, y0=Y0, t=self.x_array)

    def get_Yprime(self, Y, x):
        
        """Returns Yprime for numerical solver."""

        Yprime = np.zeros(Y.size)

        for i in range(1, self.y_nodes - 1):
            Yprime[i] = (
                self.delta_x / (4. * self.Pe) * (Y[i + 1] - 2 * Y[i] +
            Y[i + 1]) / self.delta_y ** 2
                )
        
        self.wall_flux = -self.Da * Y[0]
        Yprime[0] = (
            ((Y[1] - Y[0]) - self.wall_flux) / self.delta_y ** 2
            )
        # interface boundary condition.

        Yprime[-1] = (
            ((Y[-1] - Y[-2]) - 0) / self.delta_y ** 2
            )
        # symmetry boundary condition
