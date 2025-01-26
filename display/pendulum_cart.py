"""
Author: Miguel Tamayo

pendulum_display.py
Contains class for PyQt6 GraphicsItem in charge of drawing the robot
"""

from PyQt6.QtWidgets import (QGraphicsItem, QGraphicsLineItem)
from PyQt6.QtCore import (QRectF, Qt, QPointF)

from PyQt6.QtGui import (QPainter, QPen, QColor, QBrush)

import numpy as np

from constants.application import *
from constants.simulation import *

class PendulumCartDisplay(QGraphicsItem):
    """
    Class representing PyQt6 QGraphics widget

    inputs:
    -------
        initial_cart_x [m]: cart's initial position along the x-axis
        initial_theta [rad]: pendulum's initial angle
    """
    def __init__(self,
                 initial_theta: float = 0.0,
                 parent = None) -> None:
        super().__init__(parent)

        ### --- cart --- ###
        self.cartY = canvas_height / 2
        self.cartRect = QRectF()
        self.cartX_offset = canvas_width / 2

        ### --- pendulum --- ###
        self.y1 = self.cartY

        self.updatePendulumCart(0+self.cartX_offset, initial_theta)

    def updatePendulumCart(self, cartX: float, theta: float) -> None:
        """
        Updates the pendulum's angle

        inputs:
        -------
            cart_x [m]: cart's new x location
            theta [rad]: pendulum's new angle
        """

        # update the cart's location
        cartX = cartX+self.cartX_offset
        topLeft = QPointF(cartX-cartWidth*S, self.cartY-cartHeight*S)
        bottomRight = QPointF(cartX+cartWidth*S, self.cartY+cartHeight*S)
        self.cartRect = QRectF(topLeft, bottomRight)

        # update the pendulum's location
        self.x1 = cartX
        self.x2 = self.x1 + L * S * np.sin(theta)
        self.y2 = self.y1 + L * S * np.cos(theta)

        self.update()        
    
    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rectangle for the item. Just bound the entire canvas for now

        returns:
        --------
            boundingRect: bounding rectangle
        """

        margin = 10  # Extra space to ensure the line isn't clipped
        return QRectF(0+margin, 0+margin, canvas_width-margin, canvas_height-margin)
        # return QRectF(self.x1 - self.length - margin, self.y1 - self.length - margin, 
        #               2 * (self.length + margin), 2 * (self.length + margin))

    def paint(self, painter: QPainter, option, widget=None):
        """
        Paints the pendulum and cart on the screen
        """
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        painter.drawRect(self.cartRect)
        p1 = QPointF(self.x1, self.y1)
        p2 = QPointF(self.x2, self.y2)
        painter.drawLine(p1, p2)
        pen.setColor(QColor(255, 0, 0))
        painter.drawEllipse(p2, 10, 10)