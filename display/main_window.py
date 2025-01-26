"""
Author: Miguel Tamayo

main_window.py
Manages all teh widges on the user interface as well as the functions for interactive widgets
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QGridLayout)

from PyQt6.QtCore import QTimer

import numpy as np

from constants.application import *
from .pendulum_cart import PendulumCartDisplay
from model.pendulum_dynamics import PendulumDynamics

class MainWindow(QMainWindow):
    """
    Class representing PyQt6 window
    """
    def __init__(self) -> None:
        super().__init__()
        self.dt = 0.01
        self.t = 0
        self.t_final = 100
        self.force = 0

        initial_state = np.array([0, 0, 0.1, 0]) # [x, x_dot, theta, theta_dot]

        self.setWindowTitle("Robot Simulation")
        self.simulationPaused = True # begin with a paused simulation

        ### --- Dynamics --- ###
        self.pendulumDynamics = PendulumDynamics(state_0=initial_state, F_0=self.force, dt=self.dt)

        ### ----- pyqt6 application window ----- ###
        self.setGeometry(50, 50, window_width, window_height)

        ### ----- main widget ----- ###
        # this is the widget that takes the entire screen and split in cells
        mainWidget = QWidget()
        layout = QGridLayout()
        self.setCentralWidget(mainWidget)

        ### ----- simulation canvas widget ----- ###
        canvas = QGraphicsView(mainWidget)
        canvas.setFixedSize(canvas_width, canvas_height)

        # create scene to handle pendulum item
        self.scene = QGraphicsScene(canvas)
        self.scene.setBackgroundBrush(background_color)

        self.pendulumDisplay = PendulumCartDisplay(initial_theta= initial_state[2])
        self.scene.addItem(self.pendulumDisplay)

        canvas.setScene(self.scene) # add the scene to the canvas

        ### --- Add widgets to the main layout --- ###
        # row | column | rowSpan | ColumnSpan
        layout.addWidget(canvas, 0, 0, 2, 1)

        ### dyanmics

        ### --- Simulation Timer --- ###
        self.simulationTimer = QTimer()
        self.simulationTimer.timeout.connect(self.takeStep)
        self.simulationTimer.start(10)
    
    def takeStep(self) -> None:
        """
        Advance the simulation in time
        """
        self.t += self.dt

        self.pendulumDynamics.updateState(self.force)
        C = np.array([[1, 0, 0, 0],
                      [0, 0, 1, 0]])
        
        x, theta = self.pendulumDynamics.getState(C)

        self.pendulumDisplay.updatePendulumCart(x, theta)


        # Quick check to stop the simulation when we hit the final time
        if (self.t >= self.t_final):
            self.simulationTimer.stop()
            self.close()
            return

