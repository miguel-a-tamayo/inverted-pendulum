from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def derivatives(t, state, F, cartM, pendM, L, g):
    x, x_dot, theta, theta_dot = state
    xdd_num = F + (pendM * g * np.sin(theta) * np.cos(theta)) + (theta_dot**2 * pendM * L * np.sin(theta))
    xdd_den = cartM + pendM - (pendM * np.cos(theta)**2)
    xdd = xdd_num / xdd_den

    thetadd_num = -(xdd * np.cos(theta) + g * np.sin(theta))
    thetadd = thetadd_num / L

    return [x_dot, xdd, theta_dot, thetadd]

# Define initial state, parameters, and solve
state_0 = [0, 0, 0.1, 0]  # Initial [x, x_dot, theta, theta_dot]
params = (0, 1.0, 0.2, 0.75, 9.81)  # [F, cartM, pendM, L, g]
t_span = (0, 100)
t_eval = np.linspace(0, 100, 1000)

sol = solve_ivp(derivatives, t_span, state_0, t_eval=t_eval, args=params)

# Plot theta vs time
plt.figure(figsize=(8, 5))
plt.plot(sol.t, sol.y[2], label=r'$\theta(t)$', color='blue')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)  # Optional: Add zero reference line
plt.xlabel('Time (s)')
plt.ylabel(r'Angle $\theta$ (rad)')
plt.title('Angle of the Pendulum Over Time')
plt.legend()
plt.grid()
plt.show()