import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from random import randint


class GuessNumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Угадай число")
        self.setGeometry(100, 100, 300, 200)

        self.number = randint(1, 100)
        self.attempts = 5

        self.label = QLabel("Введите число от 1 до 100:", self)
        self.label.move(20, 20)

        self.input = QLineEdit(self)
        self.input.move(20, 50)

        self.button = QPushButton("Проверить", self)
        self.button.move(20, 80)
        self.button.clicked.connect(self.checkNumber)

        self.show()

    def checkNumber(self):
        guess = int(self.input.text())

        if guess == self.number:
            QMessageBox.information(self, "Результат", "Вы угадали число! Поздравляю!")
            self.restartGame()
        elif guess < self.number:
            self.attempts -= 1
            QMessageBox.warning(self, "Результат", f"Загаданное число больше! Осталось попыток: {self.attempts}")
        else:
            self.attempts -= 1
            QMessageBox.warning(self, "Результат", f"Загаданное число меньше! Осталось попыток: {self.attempts}")

        if self.attempts == 0:
            QMessageBox.critical(self, "Результат", "Вы проиграли! Попробуйте снова.")
            self.restartGame()

    def restartGame(self):
        self.number = randint(1, 100)
        self.attempts = 5
        self.input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GuessNumberGame()
    sys.exit(app.exec())
