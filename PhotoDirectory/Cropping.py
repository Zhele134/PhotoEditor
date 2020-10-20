import PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import ImageQt
from PyQt5.uic.properties import QtCore

from PhotoDirectory import PhotoModifier
import GUI

import sys

cropped_image = None

# Function retrieved from https://stackoverflow.com/questions/25795380/how-to-crop-a-image-and-save
class CroppingFunction(QLabel):
    # declare local variables. CroppingFunction inherits QLabel functionality
    def __init__(self, image_to_crop, parent):
        super(CroppingFunction, self).__init__()
        self.parent = parent
        #set up a new QRubberBand
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.image_to_crop = image_to_crop
        self.initUI()

    def initUI(self):
        # sets up photo displayed when GUI opens
        self.setPixmap(self.image_to_crop)

    def mousePressEvent(self, QMouseEvent):
        # sets origin of QRubberBand to position of mouse when it's clicked
        self.originQPoint = QMouseEvent.pos()
        # initiates size of QRubberBand at origin point where mouse is clicked
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        # display rubber band to user
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, QMouseEvent):
        # when mouse is dragged, update size of QRubberBand
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QMouseEvent.pos()).normalized())

    def mouseReleaseEvent(self, QMouseEvent):
        # when mouse released, hide QRubberBand
        self.currentQRubberBand.hide()
        # retrieve rectangle created within QRubberBand
        currentQRect = self.currentQRubberBand.geometry()
        # delete reference to QRubberBand when GUI closes
        self.currentQRubberBand.deleteLater()
        # retrieve cropped portion of pixmap (copies within borders of QRubberBand)
        cropQPixmap = self.pixmap().copy(currentQRect)
        # convert cropped pixmap to an image
        cropped_frompixmap = ImageQt.fromqpixmap(cropQPixmap)

        global cropped_image
        # sets global variable cropped_image to reference the cropped image
        cropped_image = cropped_frompixmap
        # update cropped photo in GUI class
        self.parent.update_after_crop()
        # close this window
        self.close()

def return_cropped_image():
    return cropped_image
