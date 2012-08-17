import numpy as np
import scipy.interpolate as interp
from scipy.optimize import curve_fit
from scipy.optimize import fsolve

def init_lambda_splines(self):

    """Sets up spline fitting for get_lambda."""

    self.lambda_splines = []

    max_terms = self.lambda_and_Da.shape[1] - 1

    for i in range(0, max_terms):
        self.lambda_splines.append(
            interp.splrep(self.lambda_and_Da[:, 0],
                          self.lambda_and_Da[:, i + 1])
            )
    self.lambda_splines = np.array(self.lambda_splines)

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

def get_eta(self, *args, **kwargs):

    """Returns conversion efficiency.

    Inputs:

    Vdot : flow rate (m^3/s)
    T : temperature (K).

    or kwargs:
    Pe
    Da

    or if none:
    self.Vdot and self.T are used

    Vdot and T are generally going to be the independent variables
    that are varied here so they need to be inputs.
    """


    if 'Pe' in kwargs:
        Pe = kwargs['Pe']

    elif len(args) == 2:
        Vdot = args[0]
        T = args[1]
        Pe = self.get_Pe(Vdot, T)

    else:
        Vdot = self.Vdot
        T = self.T
        Pe = self.get_Pe(Vdot, T)
    
    if 'Da' in kwargs:
        Da = kwargs['Da']
        A_i = self.get_A_i(Da=Da)

    elif len(args) == 2:
        T = args[1]
        A_i = self.get_A_i(T)

    else:
        T = self.T
        A_i = self.get_A_i(T)

    self.eta_array = (
        (A_i / self.lambda_i * np.sin(self.lambda_i) * (1. -
        np.exp((-self.lambda_i ** 2. / (4. * Pe)) * self.x_)))
        )

    self.eta = self.eta_array.sum()

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
        (A_i * np.exp((-lambda_i ** 2. / (4. * Pe)) * x_) *
        np.cos(lambda_i * y_)).sum()
        )

    return self.Y

def get_A_i(self, *args, **kwargs):

    """Returns pre-exponential Arrhenius coefficient.

    Inputs:

    T: temperature (K)

    or keyword argument Da from get_Da
    or keyword argument lambda_i from get_lambda
    """

    if len(args) == 1:
        T = args[0]
        lambda_i = self.get_lambda(T)

    elif 'Da' in kwargs:
        Da = kwargs['Da']
        lambda_i = self.get_lambda(Da=Da)

    elif 'lambda_i' in kwargs:
        lambda_i = kwargs['lambda_i']

    self.A_i = (
        2. * np.sin(lambda_i) / (lambda_i + np.sin(lambda_i) *
        np.cos(lambda_i))
        )

    return self.A_i

def get_lambda_spl(self, *args, **kwargs):

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

    self.lambda_i = np.zeros(self.terms)

    for i in range(self.terms):
        self.lambda_i[i] = (
            interp.splev(Da, self.lambda_splines[i])
            )

    return self.lambda_i

def get_lambda_error(self, guess, *args):

    """Returns error associated with guess of lambda.

    Inputs:
    guess: initial guess at lambda as a function of Da.

    if Da in kwargs, then Da is used
    """

    if len(args) == 1:
        Da = args[0]

    else:
        Da = self.Da

    error = 1 - guess / Da * np.tan(guess)

    return error

def get_lambda(self, *args, **kwargs):

    """Uses fsolve to represent lambda as a function of Da.

    Inputs:

    T : temperature (K)

    or keyword argument Da from get_Da
    """

    if 'Da' in kwargs:
        Da = kwargs['Da']

    else:
        T = args[0]
        Da = np.float32(self.get_Da(T))

    self.lambda_i = self.get_lambda_spl(Da=Da)
    lambda_i = self.lambda_i

    self.lambda_i = (
        fsolve(self.get_lambda_error, x0=lambda_i, args=(Da))
        )

    return self.lambda_i

