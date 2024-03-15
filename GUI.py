import sys
from PIL import Image, ImageDraw
import math
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFileDialog, QApplication, QMainWindow, QWidget, \
    QComboBox, QHBoxLayout, QSplitter


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Perler GUI'
        self.perler_colors = {}

        # Creating buttons, dropdown, and labels
        self.button = QPushButton('Select Image')
        self.button.clicked.connect(self.selectImage)
        self.dropDown = QComboBox(self)
        self.dropDown.addItem('1')
        self.dropDown.addItems([str(i * 2) for i in range(13)])
        self.dropDown.currentTextChanged.connect(self.pixelChange)
        self.imLabel = QLabel()
        self.cKeyLabel = QLabel()

        # Setting horizontal layout for the top buttons
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.button)
        self.hLayout.addWidget(self.dropDown)

        self.buttonContainer = QWidget()
        self.buttonContainer.setLayout(self.hLayout)

        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.buttonContainer)
        self.vLayout.addWidget(self.imLabel)
        self.vLayout.addWidget(self.cKeyLabel)
        self.setLayout(self.vLayout)

    def selectImage(self):
        # Opens file dialog
        imagePath, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image files (*.png *.jpg *.jpeg *.bmp '
                                                                             '*.gif)')
        if imagePath:
            self.image = imagePath
            pixelSize = int(self.dropDown.currentText())
            self.processImage(self.image, pixelSize)

    def pixelChange(self):
        # Called when pixel size value is changed
        if hasattr(self, 'image'):
            pixelSize = int(self.dropDown.currentText())
            self.processImage(self.image, pixelSize)

    def processImage(self, image, pixelSize):
        self.imLabel.clear()
        self.cKeyLabel.clear()
        self.color_counts = {}

        if image:
            self.imLabel.clear()
            self.cKeyLabel.clear()

            # Image processing done by Dylan-Lawrence
            space = 1
            with open("perler_colors.txt", "r") as f:
                for line in f:
                    line = line.rstrip('\n').split("\t")
                    self.perler_colors[line[0]] = tuple(map(int, line[1].strip('"').split(',')))

            im = Image.open(image)
            cKey = Image.new(mode='RGB', size=(360, 360))
            draw = ImageDraw.Draw(cKey)
            for i in range(im.width):
                for j in range(im.height):
                    curr = im.getpixel((i, j))

                    # Check if pixel is not transparent
                    if curr[-1] != 0:
                        deltas = [(color, math.dist(self.perler_colors[color],
                                                    curr[:3])) for color in self.perler_colors]

                        deltas.sort(key=lambda x: x[1])

                        im.putpixel((i, j), self.perler_colors[deltas[0][0]])

                        # Increment the count for this color
                        if deltas[0][0] in self.color_counts:
                            self.color_counts[deltas[0][0]] += 1 / int(pixelSize) ** 2
                        else:
                            self.color_counts[deltas[0][0]] = 1 / int(pixelSize) ** 2
            kw = 15
            kh = 15
            for color, count in self.color_counts.items():
                y0 = space * (kw + 10)
                y1 = y0 + kh
                count = round(count)
                draw.rectangle(xy=(0, y0, kw, y1),
                               fill=self.perler_colors[color],
                               outline=(0, 0, 0),
                               width=0)
                draw.text(xy=(kw + 5, y0),
                          text=f"{color}: {count}",
                          fill=(255, 255, 255))
                space += 1

            # Converting PIL image to PyQT image
            im, cKey = im.convert("RGB"), cKey.convert('RGB')
            dataIm, dataCKey = im.tobytes('raw', 'RGB'), cKey.tobytes('raw', 'RGB')
            image1 = QImage(dataIm, im.size[0], im.size[1], QImage.Format_RGB888)
            image2 = QImage(dataCKey, cKey.size[0], cKey.size[1], QImage.Format_RGB888)
            pix1 = QPixmap.fromImage(image1)
            pix2 = QPixmap.fromImage(image2)
            self.imLabel.setPixmap(pix1)
            self.cKeyLabel.setPixmap(pix2)


app = QApplication(sys.argv)
window = QMainWindow()
window.setCentralWidget(App())
window.setWindowTitle("Perler GUI")
window.show()
sys.exit(app.exec_())
