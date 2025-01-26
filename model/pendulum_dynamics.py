"""
Author: Miguel Tamayo

pendulum_dynamics.py
Implements the ODEs that represent a simple pendulum
"""

import numpy as np
from scipy.integrate import solve_ivp

from constants.simulation import *

class PendulumDynamics:
    """
    class that hold's dynamics model

    inputs:
    -------
        state_0: initial dynamics state 
        F_0 [N]: initial force acting on the cart
        dt [s]: simulation step size
    """
    def __init__(self,
                 state_0: np.array = np.zeros(4),
                 F_0: float = 0,
                 dt: float = 0.01) -> None:

        # initialize the state [x, x_dot, theta, theta_dot]
        self.state = state_0
        self.dt = dt
        self.updateState(F_0)
    
    def computeStateDerivative(self, t, state, F):
        _, x_dot, theta, theta_dot = state
        xdd_num = F + (pendM * g * np.sin(theta) * np.cos(theta)) + (theta_dot**2 * pendM * L * np.sin(theta))
        xdd_den = cartM + pendM - (pendM * np.cos(theta)**2)
        xdd = xdd_num / xdd_den

        thetadd_num = -(xdd * np.cos(theta) + g * np.sin(theta))
        thetadd = thetadd_num / L

        return [x_dot, xdd, theta_dot, thetadd]

    def updateState(self, F: float = 0.0):
        """
        Updates the system's state
        Updates the dynamics that describe the pendulum and returns the current angle
        """
        t_span = [0, self.dt] # evaluate the ODE for one time step (dt)

        solution = solve_ivp(
            self.computeStateDerivative,
            t_span,
            self.state,
            t_eval=[self.dt],
            args=(F,)
        )
    
        self.state = solution.y[:, -1]


    def getState(self, C = None) -> np.array:
        """
        Return's the desired state given a C matrix. If no matrix is given, all states will
        be returned

        inputs:
        -------
            C: Output matrix
        
        returns:
        --------
            states: States of interest
        """

        if C is None:
            states = self.state
        else:
            states = np.matmul(C, self.state.T)
            states = states.T
        
        return states