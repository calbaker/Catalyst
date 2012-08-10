"""Module for class definition for experimental data with model curve
fitting capability."""

import numpy as np
from scipy.optimize import curve_fit
import xlrd

import catalyst
reload(catalyst)

class ExpCat(object):

    """Class for keeping track of experimental data"""

    def __init__(self):
        """Sets constants and initializes parent class."""
        self.T_ambient = 300. # ambient temperature (K)

        self.p0 = np.array([5.e16, 27.e3]) 
        # initial guess at A_arr and T_a

    def set_params(self):

        """Uses scipy optimize curve_fit to determine Arrhenius
        parameters that result in best curve fit."""

        self.popt, self.pcov = curve_fit(self.get_eta_dim, self.T_exp,
        self.eta_exp, p0 = self.p0) 
        self.A_arr = self.popt[0]
        self.T_a = self.popt[1]

        self.set_eta_ij()

    def get_eta_dim(self, T, A_arr, T_a):

        """Returns species conversion efficiency, eta, as a function
        of required argument T. Used by set_params."""

        self.Pe_ij = self.get_Pe(self.Vdot, T) 
        Da = self.get_Da(T, A_arr, T_a)
        eta = self.get_eta(self.Pe_ij, Da)

        return eta

    def get_S_r(self):

        """Returns sum of residuals squared for all data points."""

        S_r = np.sum((self.eta_model - self.eta_exp)**2.)

        return S_r

    def import_data(self):

        """Imports data from excel sheet."""

        self.worksheet = xlrd.open_workbook(filename=self.source).sheet_by_index(0)
        # Import conversion data from worksheet and store as scipy arrays
        self.T_raw = np.array(
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
        
