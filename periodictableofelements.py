from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMainWindow, QTextEdit, QLineEdit
import sys
import csv

def read_csv(periodictable):
    data = []
    with open('periodictable.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def get_element_info(data, element_number):
    element_data = {}
    for i, row in enumerate(data[int(element_number) - 1]):
        key = ''
        if i == 0:
            key = 'Atomic Number'
        elif i == 1:
            key = 'Symbol'
        elif i == 2:
            key = 'Element'
        elif i == 3:
            key = 'Origin of name'
        elif i == 4:
            key = 'Group'
        elif i == 5:
            key = 'Period'
        elif i == 6:
            key = 'Atomic weight'
        elif i == 7:
            key = 'Density'
        elif i == 8:
            key = 'Melting point'
        elif i == 9:
            key = 'Boiling point'
        elif i == 10:
            key = 'Specific heat capacity'
        elif i == 11:
            key = 'Electronegativity'
        elif i == 12:
            key = 'Abundance in earth\'s crust'
        element_data[key] = row
    return element_data

class PeriodicTableApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Periodic Table of Elements")
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        self.data = read_csv('periodictable.csv')
        elements = []
        row = 0
        col = 0
        for i in range(1, len(self.data) + 1):
            element_symbol = self.data[i - 1][1]
            elements.append(element_symbol)
            button = QPushButton(element_symbol)
            button.clicked.connect(lambda checked, element_number=i: self.on_element_click(element_number))
            layout.addWidget(button, row, col)
            col += 1
            if col == 18:
                col = 0
                row += 1

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit, row + 1, 0, 1, 18)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field, row + 2, 0, 1, 18)

        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_element)
        layout.addWidget(self.search_button, row + 3, 0, 1, 18)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_element_click(self, element_number):
        element_info = get_element_info(self.data, element_number)
        info_text = ""
        for key, value in element_info.items():
            info_text += f'{key}: {value}\n'
        self.text_edit.setPlainText(info_text)

    def search_element(self):
        element_number = self.input_field.text().strip()
        if element_number.isdigit() and 1 <= int(element_number) <= len(self.data):
            self.on_element_click(int(element_number))
        else:
            self.text_edit.setPlainText("Некорректно")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeriodicTableApp()
    window.show()
    sys.exit(app.exec())
