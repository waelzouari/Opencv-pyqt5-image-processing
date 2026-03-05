from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

qtcreator_file = "design.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class DesignWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DesignWindow, self).__init__()
        self.setupUi(self)

        self.img = None
        self.img_gray = None

        self.Browse.clicked.connect(self.get_image)
        self.DisplayRedChan.clicked.connect(self.showRedChannel)
        self.DisplayGreenChan.clicked.connect(self.showGreenChannel)
        self.DisplayBlueChan.clicked.connect(self.showBlueChannel)

        self.DisplayColorHist.clicked.connect(self.show_HistColor)

        self.DisplayGrayImg.clicked.connect(self.show_UpdatedImgGray)
        self.DisplayGrayHist.clicked.connect(self.show_HistGray)

    def makeFigure(self, widget_name, pixmap):
        pixmap = pixmap.scaled(self.findChild(QtWidgets.QLabel,widget_name).width(),self.findChild(QtWidgets.QLabel,widget_name).height())
        self.findChild(QtWidgets.QLabel,widget_name).setPixmap(pixmap)

    def showDimensions(self, img):
        height = str(img.shape[0])
        width = str(img.shape[1])
        channels = str(img.shape[2])
        resultat = f" Hauteur : {height} \n Largeur : {width} \n Nombre de cannaux : {channels}"
        self.Dimensions.setText(resultat)

    def convert_cv_qt(self, cv_image):
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        cv_image_Qt_format = QtGui.QImage(cv_image.data, w, h,bytes_per_line, QtGui.QImage.Format_BGR888)
        return QPixmap.fromImage(cv_image_Qt_format)

    def get_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une image",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )

        if file_path:
            self.img = cv2.imread(file_path)
            pixmap = self.convert_cv_qt(self.img)
            self.OriginalImg.setPixmap(pixmap)
            self.OriginalImg.setScaledContents(True)
            self.showDimensions(self.img)

    def showRedChannel(self):
        if self.img is None:
            return
        b, g, r = cv2.split(self.img)
        red_img = cv2.merge([np.zeros_like(r), np.zeros_like(r), r])
        pixmap = self.convert_cv_qt(red_img)
        self.RedChannel.setPixmap(pixmap)
        self.RedChannel.setScaledContents(True)
    def showGreenChannel(self):
        if self.img is None:
            return
        b, g, r = cv2.split(self.img)
        green_img = cv2.merge([np.zeros_like(g), g, np.zeros_like(g)])
        pixmap = self.convert_cv_qt(green_img)
        self.GreenChannel.setPixmap(pixmap)
        self.GreenChannel.setScaledContents(True)
    def showBlueChannel(self):
        if self.img is None:
            return
        b, g, r = cv2.split(self.img)
        blue_img = cv2.merge([b, np.zeros_like(b), np.zeros_like(b)])
        pixmap = self.convert_cv_qt(blue_img)
        self.Bluechannel.setPixmap(pixmap)
        self.Bluechannel.setScaledContents(True)

    def show_HistColor(self):
        if self.img is None:
            return
        img = self.img
        colors = ('b', 'g', 'r')
        plt.figure()
        for i, col in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)

        plt.title("Histogramme par Canaux")
        plt.xlabel("Intensité")
        plt.ylabel("Nombre de pixels")
        plt.savefig("Color_Histogram.png")
        plt.close()

        pixmap = self.convert_cv_qt(cv2.imread("Color_Histogram.png"))
        self.ColorHist.setPixmap(pixmap)
        self.ColorHist.setScaledContents(True)

    def getContrast(self):
        c = self.Contrast.text().strip()  # enlève espaces avant/après
        if not c:
            return 1.0
        try:
            return float(c.replace(',', '.'))  # accepte 1,8 → 1.8
        except:
            return 1.0

    def getBrightness(self):
        b = self.Brightness.text().strip()
        if not b:
            return 0
        try:
            return int(float(b))  # accepte 60.0 → 60
        except:
            return 0

    def show_UpdatedImgGray(self):
        if self.img is None:
            return

        alpha = self.getContrast()
        beta = self.getBrightness()

        print(alpha, beta)

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img_gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

        gray_bgr = cv2.cvtColor(self.img_gray, cv2.COLOR_GRAY2BGR)

        self.GrayImg.setPixmap(self.convert_cv_qt(gray_bgr))
        self.GrayImg.setScaledContents(True)

    def calc_HistGray(self):
        return cv2.calcHist([self.img_gray], [0], None, [256], [0, 256])

    def show_HistGray(self):
        if self.img_gray is None:
            return
        hist = self.calc_HistGray()
        plt.figure()
        plt.plot(hist, color='black')
        plt.title("Histogramme Niveaux de Gris")
        plt.savefig("Gray_Histogram.png")
        plt.close()

        pixmap = self.convert_cv_qt(cv2.imread("Gray_Histogram.png"))
        self.GrayHist.setPixmap(pixmap)
        self.GrayHist.setScaledContents(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DesignWindow()
    window.show()
    sys.exit(app.exec_())