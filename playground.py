import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def cart_pendulum(time, state, cartM, pendM, L, g, F):
    
def cart_pendulum(t, X, M, m, L, g, F):
    x, x_dot, theta, theta_dot = X
    
    x_ddot = (F + m * g * np.sin(theta) * np.cos(theta) + m * L * theta_dot**2 * np.sin(theta)) / ((M + m) - m * np.cos(theta)**2)
    theta_ddot = -(x_ddot * np.cos(theta) + g * np.sin(theta)) / L
    
    return [x_dot, x_ddot, theta_dot, theta_ddot]

# Parameters
M = 1.0  # Mass of cart
m = 0.1  # Mass of pendulum
L = 1.0  # Length of pendulum
g = 9.81 # Gravity
F = 0.0  # External force on cart

# Initial conditions
X0 = [0.0, 0.0, np.pi/4, 0.0]  # [x, x_dot, theta, theta_dot]

# Time span
t_span = (0, 500)
t_eval = np.linspace(*t_span, 1000)

# Solve the system
sol = solve_ivp(cart_pendulum, t_span, X0, args=(M, m, L, g, F), t_eval=t_eval)

# Plot results
plt.plot(sol.t, sol.y[0])  # Plot theta over time
plt.xlabel('Time [s]')
plt.ylabel('Pendulum Angle [rad]')
plt.grid()
plt.show()
