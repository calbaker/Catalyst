import numpy as np
from scipy.integrate import odeint

def solve_numeric(self):

    """Solves for species and conversion numerically."""

    self.delta_x = self.x_array[1] - self.x_array[0]

    self.delta_y = self.y_array[1] - self.y_array[0]
    Y0 = np.ones(self.y_array.size)

    self.Yxy_num = odeint(self.get_Yprime, y0=Y0, t=self.x_array)

def set_eta_ij_num(self):

    """Sets conversion efficiency over a range of Pe and Da."""

    try:
        self.Vdot_array
    except AttributeError:
        self.Vdot_array = np.array([self.Vdot])

    self.Pe_ij = np.zeros(
        [self.Vdot_array.size, self.T_array.size]
        )
    self.Da_j = np.zeros(self.T_array.size)
    self.eta_ij_num = np.zeros(self.Pe_ij.shape)

    for i in np.arange(self.Vdot_array.size):
        for j in np.arange(self.T_array.size):

            self.Vdot = self.Vdot_array[i]
            self.T = self.T_array[j]

            self.eta_ij_num[i, j] = self.get_eta_num(self.Vdot, self.T)
            self.Da_j[j] = self.Da
            self.Pe_ij[i, j] = self.Pe

def get_eta_num(self, Vdot, T):

    """Returns conversion efficiency.

    Inputs:
    Vdot : flow rate (m^3/s)
    T : temperature (K).
    """

    self.Pe = self.get_Pe(Vdot, T)
    self.Da = self.get_Da(T)

    self.solve_numeric()

    x_array = self.x_array
    self.x_array = np.array([self.x_array[0], self.x_array[-1]])

    self.eta_num = (
        self.Yxy_num[0, :].mean() - self.Yxy_num[-1, :].mean()
        )

    self.x_array = x_array

    return self.eta_num

def get_Yprime(self, Y, x):

    """Returns Yprime for numerical solver."""

    Yprime = np.zeros(Y.size)

    # symmetry boundary condition
    Yprime[0] = (
        4. / self.Pe * (Y[1] - 2 * Y[0] + Y[1]) / self.delta_y ** 2
        )

    # in the channel
    for i in range(1, self.y_array.size - 1):
        Yprime[i] = (
            4. / self.Pe * (Y[i + 1] - 2 * Y[i] + Y[i - 1]) /
            self.delta_y ** 2
            )

    # wall BC
    Yprime[-1] = (
        8. / self.Pe * (Y[-2] - Y[-1] - self.Da * Y[-1]) /
        self.delta_y
        )

    return Yprime
