import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import random

class DiceSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Моделирование статистики бросков костей")
        self.setGeometry(100, 100, 300, 300)
        self.layout = QVBoxLayout()
        self.labels = []

        self.simulate_dice(1000000)

        for i in range(2, 13):
            label_text = f"Сумма: {i}, Вероятность: {self.results[i] * 100 / 1000000:.2f}%"
            label = QLabel(label_text)
            self.labels.append(label)
            self.layout.addWidget(label)

        self.setLayout(self.layout)

    def simulate_dice(self, num_rolls):
        self.results = {}

        for _ in range(num_rolls):
            roll_1 = random.randint(1, 6)
            roll_2 = random.randint(1, 6)
            roll_sum = roll_1 + roll_2

            if roll_sum not in self.results:
                self.results[roll_sum] = 0
            self.results[roll_sum] += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiceSimulation()
    window.show()
    sys.exit(app.exec())