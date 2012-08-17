import xlrd
import numpy as np

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
        self.T_exp[0] - 50, self.T_exp[-1] + 50, 25
        )
    self.T_array = self.T_model

