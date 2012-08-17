"""Contains class definition for catalyst."""

# Distribution libraries
import numpy as np
import types

# Local libraries
import properties as prop
reload(prop)

import analytical
reload(analytical)
import experimental
reload(experimental)
import numerical
reload(numerical)
import prop_functions
reload(prop_functions)

class Catalyst(object):

    """Class for representing catalyst reactor.

    Reactor can modeled by 1 to 4 term Fourier expansion.

    A word on units:
    Pressure is always in kPa unless otherwise specified
    Temperature ditto K ditto
    Lengths ditto m ditto"""

    def __init__(self, **kwargs):
        """Sets values of constants"""

        self.init_analytical()
        self.init_numerical()
        self.init_prop_functions()
        self.init_experimental()

        self.P = 101.325  # Pressure of flow (kPa)

        self.lambda_and_Da = np.array(
            [
                [1e-5, 3.16e-03, 3.14e+00, 6.28e+00, 9.42e+00,
            1.25e+01, 1.57e+01, 1.88e+01, 2.19e+01, 2.51e+01,
            2.82e+01],
                [1e-4, 9.99e-03, 3.14e+00, 6.28e+00, 9.42e+00,
            1.25e+01, 1.57e+01, 1.88e+01, 2.19e+01,  2.51e+01,
            2.82e+01],
                [1e-3, 0.03, 3.14, 6.28, 9.42, 12.6, 15.7, 18.8, 22.0,
            25.1, 28.3],
                [2e-3, 0.044, 3.14, 6.30, 9.42, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [3e-3, 0.055, 3.14, 6.28, 9.43, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [4e-3, 0.063, 3.14, 6.28, 9.43, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [5e-3, 0.071, 3.14, 6.28, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [6e-3, 0.0773, 3.14, 6.28, 9.43, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [7e-3, 0.0836, 3.14, 6.28, 9.43, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [8e-3, 0.0893, 3.14, 6.28, 9.43, 12.6, 15.7, 18.8,
            22.0, 25.1, 28.3],
                [9e-3, 0.0947, 3.14, 6.28, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.01, 0.010, 3.14, 6.28, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3], 
                [0.015, 0.122, 3.15, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.02,  0.141, 3.15, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.025, 0.157, 3.15, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.03,  0.172, 3.15, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.2],
                [0.04, 0.199, 3.15, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.05, 0.222, 3.16, 6.29, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.09, 0.300, 3.17, 6.30, 9.43, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3], 
                [0.1, 0.311, 3.17, 6.30, 9.44, 12.6, 15.7, 18.9, 22.0,
            25.1, 28.3],
                [0.11, 0.326, 3.18, 6.30, 9.44, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.2,  0.433, 3.20, 6.31, 9.45, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.3,  0.522, 3.23, 6.33, 9.46, 12.6, 15.7, 18.9,
            22.0, 25.1, 28.3],
                [0.4, 0.593, 3.26, 6.35, 9.47, 12.6, 15.7, 18.9, 22.0,
            25.1, 28.3],
                [0.5, 0.653, 3.29, 6.36, 9.48, 12.6, 15.7, 18.9, 22.0,
            25.2, 28.3],
                [1.0, 0.860, 3.43, 6.44, 9.53, 12.6, 15.8, 18.9, 22.0,
            25.2, 28.3],
                [5.,  1.31, 4.03, 6.91, 9.89, 12.9, 16.0, 19.1, 22.2,
            25.3, 28.4],
                [10.0,  1.43, 4.31, 7.23, 10.2, 13.2, 16.3, 19.3,
            22.4, 25.5, 28.6]
                ]
            )
        # Graphically determined eigenvalues corresponding to Da.
        # First column is Da, second column is lamba_0, third column
        # is lambda_1, and so on...

        self.init_lambda_splines()

        if 'terms' in kwargs:
            self.terms = kwargs['terms']
        else:
            self.terms = 4

        self.A_arr = 11.29e6
        # Arrhenius coefficient (1/s ???)
        self.T_a = 6543.  # activation temperature (K)

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

        self.y_ = 1.

        self.x_array = np.linspace(0, self.x_, 100)
        self.y_array = np.linspace(0, self.y_ * 51 / 50, 50)

        self.T_ambient = 300. + 273.15
        # ambient temperature (K) at which flow rate is measured

        self.fuel = prop.ideal_gas(species='C3H8')
        self.air = prop.ideal_gas()
        self.air.P = self.P
        self.fuel.P = self.P

    def init_analytical(self):
        
        """Adds methods for analytical model."""        
        
        self.init_lambda_splines = (
            types.MethodType(analytical.init_lambda_splines, self)
            )
        self.set_eta_ij = types.MethodType(analytical.set_eta_ij, self)
        self.get_eta = types.MethodType(analytical.get_eta, self)
        self.get_eta_fit = types.MethodType(
            analytical.get_eta_fit, self
            )
        self.get_Y = types.MethodType(analytical.get_Y, self)
        self.get_A_i = types.MethodType(analytical.get_A_i, self)
        self.get_lambda_spl = (
            types.MethodType(analytical.get_lambda_spl, self)
            )
        self.get_lambda_error = (
            types.MethodType(analytical.get_lambda_error, self)
            )
        self.get_lambda = types.MethodType(analytical.get_lambda, self)

        
    def init_numerical(self):
        
        """Adds methods from numerical."""

        self.solve_numeric = types.MethodType(numerical.solve_numeric,
        self)
        self.set_eta_ij_num = (
            types.MethodType(numerical.set_eta_ij_num, self)
            )
        self.get_eta_num = types.MethodType(numerical.get_eta_num,
        self)
        self.get_Yprime = types.MethodType(numerical.get_Yprime, self)


    def init_prop_functions(self):
        
        """Adds methods from prop_functions."""

        self.get_Da = types.MethodType(prop_functions.get_Da, self)
        self.get_thiele = types.MethodType(prop_functions.get_thiele, self)
        self.get_k = types.MethodType(prop_functions.get_k, self)
        self.get_Pe = types.MethodType(prop_functions.get_Pe, self)
        self.set_TempPres_dependents = (
            types.MethodType(prop_functions.set_TempPres_dependents, self)
            )
        self.get_mfp = types.MethodType(prop_functions.get_mfp, self)
        self.get_Kn = types.MethodType(prop_functions.get_Kn, self)
        self.get_D_C3H8_air_eff = (
            types.MethodType(prop_functions.get_D_C3H8_air_eff, self)
            )
        self.get_D_C3H8_air_Kn = (
            types.MethodType(prop_functions.get_D_C3H8_air_Kn, self)
            )
        self.get_D_C3H8_air = (
            types.MethodType(prop_functions.get_D_C3H8_air, self)
            )

    def init_experimental(self):
        
        """Adds methods from experimental."""
        
        self.get_S_r = types.MethodType(experimental.get_S_r, self)
        self.import_data = types.MethodType(
            experimental.import_data, self
            ) 
        self.set_fit_params = types.MethodType(
            experimental.set_fit_params, self
            )
