import sys
from PyQt6.QtWidgets import *
from reportlab.lib.pagesizes import *
from reportlab.pdfgen import canvas
from reportlab.lib import *
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import *
import os, math

font_size = 36
table_size = 1.25 * font_size
cell_size = table_size / 2
font_name = "NotoSansJP-regular"
font_path = font_name + '.ttf'
A4_x_start = 90
A4_y_start = 770
x_start_temp = A4_x_start
y_start_temp = A4_y_start
kanji_amount = 0
row = 1
kanji = ""
filename = "output_kanji.pdf"
c = canvas.Canvas(filename, pagesize=A4)

def draw_kanji(kanji, gray, repeat):
        global c, row, x_start_temp, y_start_temp
        
        is_first = True
        for j in range(repeat):
            if x_start_temp + table_size > 500:
                row += 1
                x_start_temp = A4_x_start
                y_start_temp -= table_size

            if y_start_temp - table_size < 70:
                c.showPage()
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                c.setFont(font_name, font_size)
                row = 1
                x_start_temp = A4_x_start
                y_start_temp = A4_y_start

            for k in range(3):
                    if k == 1:
                        c.setDash(3,3)
                        c.setStrokeColor(lightgrey)
                    else:
                        c.setDash()
                        c.setStrokeColor(black)
                    c.line(x_start_temp, y_start_temp - k * cell_size, x_start_temp + table_size, y_start_temp - k * cell_size)
                    c.line(x_start_temp + k * cell_size, y_start_temp, x_start_temp + k * cell_size, y_start_temp - table_size)

            text_width = pdfmetrics.stringWidth(kanji, font_name, font_size)
            text_x = x_start_temp + cell_size - text_width / 1.95
            text_y = y_start_temp - cell_size - font_size / 2.5
            x_start_temp += table_size
            
            if is_first:
                c.setFillColor(black)
                is_first = False
            elif j > gray:
                continue
            else:
                c.setFillColor(darkgray)

            c.drawString(text_x, text_y, kanji)
        x_start_temp = A4_x_start
        y_start_temp -= 20 + table_size

class SimpleApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        c.setFont(font_name, font_size)
        self.groupBox = QGroupBox("Kanji sheet")

        self.kanji_display = QLabel("", self)
        self.kanji_display.setStyleSheet("font-size: 24px;") 

        self.amount_lbl = QLabel("Traces")
        self.amount_edit = QSpinBox()
        self.amount_edit.setMaximum(100)
        self.amount_edit.setValue(8)
        self.amount_edit.setMinimum(1)

        self.empty_lbl = QLabel("Empty")
        self.empty_edit = QSpinBox()
        self.empty_edit.setMaximum(200)
        self.empty_edit.setValue(18)
        self.empty_edit.setMinimum(1)

        layout = QVBoxLayout()

        self.kanji_edit = QLineEdit(self)
        self.add = QPushButton('Add more')
        self.btn = QPushButton('Save')
        self.add.clicked.connect(self.add_more)
        self.btn.clicked.connect(self.create_pdf)
        kanji = self.kanji_edit.text()
        self.kanji_edit.setPlaceholderText("Sign")

        layout.addWidget(self.kanji_edit)
        layout.addWidget(self.kanji_display) 

        layout.addWidget(self.amount_lbl)
        layout.addWidget(self.amount_edit)
        
        layout.addWidget(self.empty_lbl)
        layout.addWidget(self.empty_edit)
        
        layout.addWidget(self.add)
        layout.addWidget(self.btn)
        layout.addStretch(1)

        self.groupBox.setLayout(layout)
        self.setLayout(layout)

        self.setWindowTitle('Kanji App')
        self.setGeometry(100, 100, 300, 300)

    def add_more(self):
        global kanji, kanji_amount, c
        if self.kanji_edit.text() == "":
            return
        kanji_amount += 1
        kanji = self.kanji_edit.text() 
        self.kanji_display.setText(kanji)
        self.kanji_edit.setText("")
        draw_kanji(kanji, int(self.amount_edit.text()), int(self.amount_edit.text()) + int(self.empty_edit.text()) + 1)

    def create_pdf(self):
        global kanji, kanji_amount, c

        if self.kanji_edit.text() == "" and kanji_amount == 0:
            return
        elif self.kanji_edit.text() == "" and kanji_amount > 0:
            c.save()
            return
                
        kanji = self.kanji_edit.text() 
        kanji_amount += 1
        self.kanji_display.setText(kanji)
        self.kanji_edit.setText("")

        draw_kanji(kanji, int(self.amount_edit.text()), int(self.amount_edit.text()) + int(self.empty_edit.text()) + 1)
        c.save()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())