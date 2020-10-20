import PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import ImageQt

from PhotoDirectory import PhotoModifier
from PhotoDirectory import Filters
from PhotoDirectory import Cropping

import sys

from PhotoDirectory import Cropping, PhotoModifier

# constants
MIN_BUTTON_WIDTH = 200

SLIDER_MINIMUM = 50
SLIDER_MAXIMUM = 150
SLIDER_DEFAULT = 100
BLUR_DEFAULT = 0
BLUR_MIN = 0
BLUR_MAX = 10

img_with_changes = None
img_original = None
img_with_crop = None


class ImageValues:
    def __init__(self):
        self.brightness = 0
        self.contrast = 0
        self.sharpness = 0
        self.blur_radius = 0

        self.horizontal_flip = False
        self.vertical_flip = False
        self.rotate_angle = 0

        self.filter_name = None

    def reset(self):
        self.brightness = 0
        self.contrast = 0
        self.sharpness = 0
        self.blur_radius = 0

        self.filter_name = None

        self.horizontal_flip = False
        self.vertical_flip = False
        self.rotate_angle = 0


image_values = ImageValues()


def get_photo_with_all_changes():
    brightness = image_values.brightness
    contrast = image_values.contrast
    sharpness = image_values.sharpness
    blur = image_values.blur_radius
    rotate_angle = image_values.rotate_angle

    image = img_with_changes

    if brightness != 0:
        image = PhotoModifier.brighten(image, brightness)

    if contrast != 0:
        image = PhotoModifier.contrast(image, contrast)

    if sharpness != 0:
        image = PhotoModifier.sharpen(image, sharpness)

    if blur != 0:
        image = PhotoModifier.blur(image, blur)

    if rotate_angle:
        image = PhotoModifier.rotate_image(image, rotate_angle)

    if image_values.horizontal_flip:
        image = PhotoModifier.flip_image_horizontally(image)

    if image_values.vertical_flip:
        image = PhotoModifier.flip_image_vertically(image)

    return image

def change_img_with_changes():
    CroppingTab.update_after_crop()


class EditTabsWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.filters_tab = FiltersTab(self)
        self.sliders_tab = SlidersTab(self)
        self.cropping_tab = CroppingTab(self)
        self.transpose_tab = TransposeTab(self)

        self.addTab(self.filters_tab, "Filters")
        self.addTab(self.sliders_tab, "Adjustments")
        self.addTab(self.cropping_tab, "Cropping")
        self.addTab(self.transpose_tab, "Transpose")

        self.setMinimumHeight(300)


class FiltersTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QGridLayout()

        self.normalButton = QPushButton("Normal")
        self.normalButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.normalButton.clicked.connect(lambda: self.set_filter_on_click("Normal"))

        self.greyscaleButton = QPushButton("Greyscale")
        self.greyscaleButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.greyscaleButton.clicked.connect(lambda: self.set_filter_on_click("Greyscale"))

        self.negativeButton = QPushButton("Negative")
        self.negativeButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.negativeButton.clicked.connect(lambda: self.set_filter_on_click("Negative"))

        self.crimsonButton = QPushButton("Crimson")
        self.crimsonButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.crimsonButton.clicked.connect(lambda: self.set_filter_on_click("Crimson"))

        self.sepiaButton = QPushButton("Sepia")
        self.sepiaButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.sepiaButton.clicked.connect(lambda: self.set_filter_on_click("Sepia"))

        self.BWButton = QPushButton("Black&White")
        self.BWButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.BWButton.clicked.connect(lambda: self.set_filter_on_click("BlackAndWhite"))

        layout.addWidget(self.normalButton, 0, 0)
        layout.addWidget(self.greyscaleButton, 0, 1)
        layout.addWidget(self.BWButton, 0, 2)
        layout.addWidget(self.negativeButton, 1, 0)
        layout.addWidget(self.sepiaButton, 1, 1)
        layout.addWidget(self.crimsonButton, 1, 2)

        self.setLayout(layout)

    def set_filter_on_click(self, name):
        global img_with_changes
        global img_with_crop
        global img_original
        if (name == "Normal"):
            if (img_with_crop):
                img_with_changes = img_with_crop
            else:
                img_with_changes = img_original
        else:
            img_with_changes = PhotoModifier.filter_photo(img_with_changes, name)
        self.parent.parent.replace_imgLabel()


class SlidersTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        slider_layout = QVBoxLayout()
        slider_layout.setAlignment(Qt.AlignCenter)


        self.bright_label = QLabel("Adjust Brightness")
        self.bright_label.setAlignment(Qt.AlignCenter)
        self.brighten_slider = QSlider(Qt.Horizontal)
        self.brighten_slider.setMinimum(SLIDER_MINIMUM)
        self.brighten_slider.setMaximum(SLIDER_MAXIMUM)
        self.brighten_slider.setValue(SLIDER_DEFAULT)
        self.brighten_slider.sliderReleased.connect(self.set_brightness_on_release)

        self.contrast_label = QLabel("Adjust Contrast")
        self.contrast_label.setAlignment(Qt.AlignCenter)
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(SLIDER_MINIMUM)
        self.contrast_slider.setMaximum(SLIDER_MAXIMUM)
        self.contrast_slider.setValue(SLIDER_DEFAULT)
        self.contrast_slider.sliderReleased.connect(self.set_contrast_on_release)

        self.sharpen_label = QLabel("Adjust Sharpness")
        self.sharpen_label.setAlignment(Qt.AlignCenter)
        self.sharpen_slider = QSlider(Qt.Horizontal)
        self.sharpen_slider.setMinimum(SLIDER_MINIMUM)
        self.sharpen_slider.setMaximum(SLIDER_MAXIMUM)
        self.sharpen_slider.setValue(SLIDER_DEFAULT)
        self.sharpen_slider.sliderReleased.connect(self.set_sharpness_on_release)

        self.blur_label = QLabel("Adjust Blur")
        self.blur_label.setAlignment(Qt.AlignCenter)
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setMinimum(BLUR_MIN)
        self.blur_slider.setMaximum(BLUR_MAX)
        self.blur_slider.setValue(BLUR_DEFAULT)
        self.blur_slider.sliderReleased.connect(self.set_blur_on_release)

        slider_layout.addWidget(self.bright_label)
        slider_layout.addWidget(self.brighten_slider)
        slider_layout.addWidget(self.contrast_label)
        slider_layout.addWidget(self.contrast_slider)
        slider_layout.addWidget(self.sharpen_label)
        slider_layout.addWidget(self.sharpen_slider)
        slider_layout.addWidget(self.blur_label)
        slider_layout.addWidget(self.blur_slider)

        self.setLayout(slider_layout)

    def set_brightness_on_release(self):
        self.brighten_slider.setToolTip(str(self.brighten_slider.value()/100))
        image_values.brightness = self.brighten_slider.value()/100
        self.parent.parent.replace_imgLabel()

    def set_contrast_on_release(self):
        self.contrast_slider.setToolTip(str(self.contrast_slider.value()/100))
        image_values.contrast = self.contrast_slider.value()/100
        self.parent.parent.replace_imgLabel()

    def set_sharpness_on_release(self):
        self.sharpen_slider.setToolTip(str(self.sharpen_slider.value()/100))
        image_values.sharpness = self.sharpen_slider.value()/100
        self.parent.parent.replace_imgLabel()

    def set_blur_on_release(self):
        self.blur_slider.setToolTip(str(self.blur_slider.value()))
        image_values.blur_radius = self.blur_slider.value()
        self.parent.parent.replace_imgLabel()

    def reset_sliders(self):
        self.brighten_slider.setValue(SLIDER_DEFAULT)
        self.contrast_slider.setValue(SLIDER_DEFAULT)
        self.sharpen_slider.setValue(SLIDER_DEFAULT)
        self.blur_slider.setValue(BLUR_DEFAULT)


class CroppingTab(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.startButton = QPushButton("Start Cropping")
        self.startButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.startButton.clicked.connect(self.start_cropping)

        cropping_layout = QVBoxLayout()
        cropping_layout.addWidget(self.startButton)
        self.setLayout(cropping_layout)

    def start_cropping(self):
        image = get_photo_with_all_changes()
        updated_image = ImageQt.toqpixmap(image)
        self.croppedWindow = Cropping.CroppingFunction(updated_image, self)
        self.croppedWindow.show()

    def update_after_crop(self):
        global img_with_changes
        global img_with_crop
        img_with_changes = Cropping.return_cropped_image()
        img_with_crop = Cropping.return_cropped_image()
        self.parent.parent.replace_imgLabel()


class TransposeTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.rotateLabel = QLabel("Rotate 90°")
        self.rotateLabel.setAlignment(Qt.AlignCenter)
        self.flipLabel = QLabel("Flip")
        self.flipLabel.setAlignment(Qt.AlignCenter)

        self.rotateLeftButton = QPushButton("Left")
        self.rotateLeftButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.rotateLeftButton.clicked.connect(self.rotate_left_on_press)

        self.rotateRightButton = QPushButton("Right")
        self.rotateRightButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.rotateRightButton.clicked.connect(self.rotate_right_on_press)

        self.flipHorizontalButton = QPushButton("Horizontally")
        self.flipHorizontalButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.flipHorizontalButton.clicked.connect(self.flip_horizontally_on_press)

        self.flipVerticalButton = QPushButton("Vertically")
        self.flipVerticalButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.flipVerticalButton.clicked.connect(self.flip_vertically_on_press)

        self.rotate_layout = QVBoxLayout()
        self.rotate_layout.addWidget(self.rotateLabel)
        self.rotate_layout.addWidget(self.rotateRightButton)
        self.rotate_layout.addWidget(self.rotateLeftButton)

        self.flip_layout = QVBoxLayout()
        self.flip_layout.addWidget(self.flipLabel)
        self.flip_layout.addWidget(self.flipHorizontalButton)
        self.flip_layout.addWidget(self.flipVerticalButton)

        transpose_layout = QHBoxLayout()
        transpose_layout.addLayout(self.rotate_layout)
        transpose_layout.addLayout(self.flip_layout)

        self.setLayout(transpose_layout)

    def rotate_left_on_press(self):
        if image_values.rotate_angle == 270:
            image_values.rotate_angle = 0
        else:
            image_values.rotate_angle += 90
        self.parent.parent.replace_imgLabel()

    def rotate_right_on_press(self):
        if image_values.rotate_angle == -270:
            image_values.rotate_angle = 0
        else:
            image_values.rotate_angle -= 90
        self.parent.parent.replace_imgLabel()

    def flip_horizontally_on_press(self):
        image_values.horizontal_flip = not image_values.horizontal_flip
        self.parent.parent.replace_imgLabel()

    def flip_vertically_on_press(self):
        image_values.vertical_flip = not image_values.vertical_flip
        self.parent.parent.replace_imgLabel()




class mainLayout(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.imgLabel = QLabel("<b>Upload</b> an image to start editing <br>"
                               "<div style = 'margin: 10px'><img src = 'transparentCamera.png' /><div>")
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.imgLabel.setContentsMargins(20, 50, 20, 10)

        self.uploadButton = QPushButton("Upload")
        self.uploadButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.uploadButton.clicked.connect(self.upload_tasks)

        self.saveButton = QPushButton("Save")
        self.saveButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.saveButton.clicked.connect(self.save_image)

        self.restartButton = QPushButton("Restart")
        self.restartButton.setMinimumWidth(MIN_BUTTON_WIDTH)
        self.restartButton.clicked.connect(self.reset_picture)

        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignTop)
        buttonLayout.addWidget(self.uploadButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.restartButton)
        buttonLayout.setSpacing(20)

        self.edit_tabs_layout = EditTabsWidget(self)
        self.edit_tabs_layout.setVisible(False)

        self.addLayout(buttonLayout)
        self.addWidget(self.imgLabel)
        self.addStretch()

        self.addWidget(self.edit_tabs_layout)

    def replace_imgLabel(self):
        image = get_photo_with_all_changes()
        updated_image = ImageQt.toqpixmap(image)
        self.imgLabel.setPixmap(updated_image)

    def upload_tasks(self):
        img_path, _ = QFileDialog.getOpenFileName(self.parent, "Upload Photo", "C:\\Pictures",
                                                  "Image files (*.jpg *.png)")
        if img_path:
            uploaded_pic = QPixmap(img_path)
            self.imgLabel.setPixmap(uploaded_pic)
            self.imgLabel.setScaledContents(True)
            self.imgLabel.setContentsMargins(20, 30, 20, 10)
            self.edit_tabs_layout.setVisible(True)

            global img_original
            img_original = ImageQt.fromqpixmap(uploaded_pic)

            global img_with_changes
            img_with_changes = img_original.copy()

            image_values.reset()

    def save_image(self):
        savefileName, _ = QFileDialog.getSaveFileName(self.parent, "QFileDialog.getSaveFileName()", "",
                                                  "Image Files (*.jpg *.png")
        if savefileName:
            image = get_photo_with_all_changes()
            image.save(savefileName)


    def reset_picture(self):
        global img_original
        global img_with_changes
        img_with_changes = img_original.copy()
        image_values.reset()
        self.replace_imgLabel()
        self.edit_tabs_layout.sliders_tab.reset_sliders()


class startWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 750)
        self.setMaximumSize(1100, 1200)
        self.setGeometry(500, 500, 750, 950)
        self.mainLayout = mainLayout(self)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Practice Photo Editor")
        self.move_window_to_center()
        self.show()

    # method from https://pythonprogramminglanguage.com/pyqt5-center-window/
    def move_window_to_center(self):
        # retrieve geometry of window
        qtRectangle = self.frameGeometry()
        # retrieve center of screen
        centerPoint = QDesktopWidget().availableGeometry().center()
        # move window to center of screen on center point
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = startWindow()

    ###This block of code produces error output for the GUI
    # Method from https://stackoverflow.com/questions/34363552/python-process-finished-with-
    # exit-code-1-when-using-pycharm-and-pyqt5
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook
    ###

    sys.exit(app.exec_())
