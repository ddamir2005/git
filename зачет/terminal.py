import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem, QCheckBox
import sqlite3
from datetime import datetime

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных
        self.init_database()

        # Создание интерфейса
        self.init_ui()

    def init_database(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                card_number INTEGER,
                                first_name TEXT,
                                last_name TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                exit_timestamp DATETIME DEFAULT NULL,
                                hours_limit INTEGER,
                                parking_employee INTEGER,
                                parking_guest INTEGER)''')
        self.conn.commit()

        self.parkings_employee = 1
        self.parkings_guests = 1

    def init_ui(self):
        self.setWindowTitle('Имитация терминала охранника')
        self.setGeometry(100, 100, 1000, 700)

        self.card_number_label = QLabel('Номер пропуска:')
        self.card_number_edit = QLineEdit(self)

        self.hours_limit_label = QLabel('Лимит часов:')
        self.hours_limit_edit = QLineEdit(self)

        self.first_name_label = QLabel('Имя:')
        self.first_name_edit = QLineEdit(self)

        self.last_name_label = QLabel('Фамилия:')
        self.last_name_edit = QLineEdit(self)

        self.action_label = QLabel('Действие:')
        self.action_radio_in = QRadioButton('Вход', self)
        self.action_radio_out = QRadioButton('Выход', self)
        self.action_group = QButtonGroup(self)
        self.action_group.addButton(self.action_radio_in)
        self.action_group.addButton(self.action_radio_out)

        self.parking_need_label = QLabel('Парковка:')
        self.parking_need_edit = QCheckBox(self)

        self.submit_button = QPushButton('Сохранить', self)
        self.submit_button.clicked.connect(self.submit_data)

        # Создание таблицы
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(9)

        # Заголовки столбцов
        headers = ['ID', 'Card Number', 'First Name', 'Last Name','Время входа', 'Время выхода', "Лимит", "Парковка С", "Парковка Г"]
        self.table_widget.setHorizontalHeaderLabels(headers)

        layout = QVBoxLayout()
        layout.addWidget(self.card_number_label)
        layout.addWidget(self.card_number_edit)
        layout.addWidget(self.hours_limit_label)
        layout.addWidget(self.hours_limit_edit)
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_edit)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_edit)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_radio_in)
        layout.addWidget(self.action_radio_out)
        layout.addWidget(self.parking_need_label)
        layout.addWidget(self.parking_need_edit)
        layout.addWidget(self.submit_button)

        # Обновление содержимого таблицы
        self.update_table()

        # Добавление таблицы в макет
        layout.addWidget(self.table_widget)

        # парковки
        self.parkings_label = QLabel('Парковки')
        layout.addWidget(self.parkings_label)
        self.parkings_table_widget = QTableWidget(self)
        self.parkings_table_widget.setColumnCount(2)
        self.parkings_table_widget.verticalHeader().setVisible(False)
        parkings_headers = ['Для сотрудников', 'Гостевые']
        self.parkings_table_widget.setHorizontalHeaderLabels(parkings_headers)
        self.update_parkings_table()
        layout.addWidget(self.parkings_table_widget)

        self.setLayout(layout)

    def update_parkings_table(self):
        self.parkings_table_widget.setRowCount(1)
        employee_parking_count = self.employee_parking_count()
        guest_parking_count = self.guest_parking_count()
        parkings_employee_item = QTableWidgetItem(str(employee_parking_count))
        parkings_guests_item = QTableWidgetItem(str(guest_parking_count))
        self.parkings_table_widget.setItem(0, 0, parkings_employee_item)
        self.parkings_table_widget.setItem(0, 1, parkings_guests_item)
        self.parkings_table_widget.update()


    def update_table(self):
        # Очищаем таблицу
        self.table_widget.setRowCount(0)

        # Получаем данные из базы данных
        self.cursor.execute('SELECT * FROM attendance')
        data = self.cursor.fetchall()

        # Заполняем таблицу данными из базы данных
        for row_number, row_data in enumerate(data):
            self.table_widget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                self.table_widget.setItem(row_number, column_number, item)

        # Обновляем виджет
        self.table_widget.update()

    def submit_data(self):
        card_number = self.card_number_edit.text()
        hours_limit = self.hours_limit_edit.text()
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        action = "Вход" if self.action_radio_in.isChecked() else "Выход"
        is_guest = 1 if hours_limit else 0
        parking_need = 1 if self.parking_need_edit.isChecked() else 0

        # Проведение проверок данных
        if not card_number or not first_name or not last_name or not action:
            self.show_message('Error', 'All fields must be filled.')
            return

        try:
            card_number = int(card_number)
            # Проверка длины номера пропуска
            if not 1 <= len(str(card_number)) <= 5:
                raise ValueError("Пропуск должен быть длиной от 1 до 5 символов.")
        except ValueError:
            self.show_message('Error', 'Пропуск должен быть числом от 1 до 5 символов.')
            return

        # Проверка, что имя и фамилия содержат только буквы
        try:
            if not first_name.isalpha() or not last_name.isalpha():
                raise ValueError("Имя и фамилия должны содержать только буквы.")
        except ValueError as e:
            self.show_message('Error', str(e))
            return

        # проверка парковок
        parking_employee = 0
        parking_guest = 0
        if parking_need:
            if is_guest:
                if self.guest_parking_count() > 0:
                    parking_guest = 1
                else:
                    self.show_message('Ошибка', 'Доступных гостевых парковок больше нет')
                    return
            else:
                # return False

                if self.employee_parking_count() > 0:

                    parking_employee = 1
                else:
                    if self.guest_parking_count() > 0:
                        parking_guest = 1
                    else:
                        self.show_message('Ошибка', 'Доступных парковок больше нет')
                        return

        # Сохранение данных в базу данных
        if action == "Вход":
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('INSERT INTO attendance (card_number, first_name, last_name, hours_limit, timestamp, parking_employee, parking_guest) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (card_number, first_name, last_name, hours_limit, timestamp, parking_employee, parking_guest))
            self.conn.commit()
        elif action == "Выход":
            self.cursor.execute('SELECT id,hours_limit FROM attendance WHERE card_number = ? ORDER BY timestamp DESC LIMIT 1',
                                (card_number,))
            entry = self.cursor.fetchone()

            if entry:
                exit_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute('UPDATE attendance SET exit_timestamp = ? WHERE id = ?', (exit_timestamp, entry[0]))
                self.conn.commit()

                if entry[1]:
                    limit_hours_at_entry = entry[1]
                    hours_difference = self.calculate_hours_difference(entry[0], exit_timestamp)

                    if hours_difference > limit_hours_at_entry:
                        self.show_message('Внимание', 'Превышен лимит часов. Обратитесь к старшему сотруднику охранной службы.')
            else:
                self.show_message('Ошибка', 'Не найден вход.')
                return
        self.update_table()
        self.update_parkings_table()

        self.show_message('Success', 'Сохранение успешно.')

        self.card_number_edit.clear()
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.hours_limit_edit.clear()
        self.parking_need_edit.setChecked(False)
        self.action_group.setExclusive(False)
        self.action_radio_in.setChecked(False)
        self.action_radio_out.setChecked(False)
        self.action_group.setExclusive(True)


    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def calculate_hours_difference(self, entry_id, exit_timestamp):
        self.cursor.execute('SELECT timestamp FROM attendance WHERE id = ?', (entry_id,))
        entry_timestamp = self.cursor.fetchone()[0]

        entry_datetime = datetime.strptime(entry_timestamp, '%Y-%m-%d %H:%M:%S')
        exit_datetime = datetime.strptime(exit_timestamp, '%Y-%m-%d %H:%M:%S')

        hours_difference = (exit_datetime - entry_datetime).seconds // 3600

        return hours_difference

    def employee_parking_count(self):
        self.cursor.execute('SELECT count(*) FROM attendance WHERE parking_employee = 1 AND exit_timestamp IS NULL')
        busy_employee_parkings = self.cursor.fetchone()[0]
        return self.parkings_employee - busy_employee_parkings

    def guest_parking_count(self):
        self.cursor.execute('SELECT count(*) FROM attendance WHERE parking_guest = 1 AND exit_timestamp IS NULL')
        busy_guest_parkings = self.cursor.fetchone()[0]
        return self.parkings_guests - busy_guest_parkings

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

if __name__ == '__main__':
    sys._excepthook = sys.excepthook

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")
    # sys.exit(app.exec())
