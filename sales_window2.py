import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView,
                             QHeaderView, QMessageBox, QAbstractItemView)
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загрузка UI файла
        ui_file_path = os.path.join(os.path.dirname(__file__), "продажи — ко222пия.ui")
        uic.loadUi(ui_file_path, self)

        # Инициализация данных
        self.cart_items = []
        self.total_amount = 0

        # Настройка таблиц
        self.setup_tables()

        # Подключение сигналов
        self.connect_signals()

        # Загрузка тестовых данных
        self.load_sample_data()

    def setup_tables(self):
        """Настройка таблиц товаров и корзины"""

        # Таблица товаров
        self.products_model = QStandardItemModel()
        self.products_model.setHorizontalHeaderLabels(["ID", "Название", "Артикул", "Цена", "В наличии"])
        self.productsTable.setModel(self.products_model)
        self.productsTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Настройка ширины колонок для таблицы товаров
        header = self.productsTable.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        # Таблица корзины
        self.cart_model = QStandardItemModel()
        self.cart_model.setHorizontalHeaderLabels(["Товар", "Кол-во", "Цена", "Сумма"])
        self.cartTable.setModel(self.cart_model)
        self.cartTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Настройка ширины колонок для корзины
        cart_header = self.cartTable.horizontalHeader()
        cart_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cart_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        cart_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        cart_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    def connect_signals(self):
        """Подключение сигналов кнопок"""
        self.addButton.clicked.connect(self.add_to_cart)
        self.removeButton.clicked.connect(self.remove_from_cart)
        self.clearButton.clicked.connect(self.clear_cart)
        self.createSaleButton.clicked.connect(self.create_sale)
        self.search_button.clicked.connect(self.search_products)
        self.filter.clicked.connect(self.show_filters)

        # Кнопки навигации
        self.sales.clicked.connect(lambda: self.switch_section("Продажи"))
        self.storage.clicked.connect(lambda: self.switch_section("Склад"))
        self.purchase.clicked.connect(lambda: self.switch_section("Закупка"))

        # Поиск по нажатию Enter
        self.searchInput.returnPressed.connect(self.search_products)

    def load_sample_data(self):
        """Загрузка тестовых данных товаров"""
        sample_products = [
            [1, "Смартфон Samsung Galaxy S23", "SMG-S23-BLK", 79990, 15],
            [2, "Ноутбук ASUS VivoBook 15", "AS-VB15-X515", 54990, 8],
            [3, "Наушники Sony WH-1000XM4", "SNY-WH-XM4", 24990, 25],
            [4, "Планшет Apple iPad Air", "APP-IPA-AIR5", 65990, 12],
            [5, "Умные часы Apple Watch SE", "APP-AW-SE2", 25990, 18],
            [6, "Фотоаппарат Canon EOS R50", "CAN-EOS-R50", 89990, 6],
            [7, "Игровая консоль PlayStation 5", "SONY-PS5-STD", 64990, 5],
            [8, "Монитор Dell 27\" S2721HS", "DEL-S2721HS", 32990, 10],
            [9, "Клавиатура Logitech MX Keys", "LOG-MX-KEYS", 8990, 30],
            [10, "Мышь Razer DeathAdder V2", "RZ-DA-V2", 4990, 22]
        ]

        for product in sample_products:
            items = [QStandardItem(str(item)) for item in product]
            # Выравнивание числовых колонок по правому краю
            items[0].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[4].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.products_model.appendRow(items)

    def get_product_stock(self, product_id):
        """Получить текущее количество товара на складе"""
        for row in range(self.products_model.rowCount()):
            if int(self.products_model.item(row, 0).text()) == product_id:
                return int(self.products_model.item(row, 4).text())
        return 0

    def update_product_stock(self, product_id, new_stock):
        """Обновить количество товара на складе"""
        for row in range(self.products_model.rowCount()):
            if int(self.products_model.item(row, 0).text()) == product_id:
                # Получаем элемент и обновляем его текст
                stock_item = self.products_model.item(row, 4)
                if stock_item:
                    stock_item.setText(str(new_stock))

                    # Сбрасываем стиль перед применением нового
                    stock_item.setBackground(Qt.GlobalColor.white)
                    stock_item.setForeground(Qt.GlobalColor.black)

                    # Меняем цвет если товара мало
                    if new_stock <= 3:
                        stock_item.setBackground(Qt.GlobalColor.red)
                        stock_item.setForeground(Qt.GlobalColor.white)
                    elif new_stock <= 10:
                        stock_item.setBackground(Qt.GlobalColor.yellow)

                    # Обновляем выравнивание
                    stock_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                break

    def add_to_cart(self):
        """Добавление выбранного товара в корзину"""
        selection = self.productsTable.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите товар из списка!")
            return

        row = selection[0].row()
        product_id = int(self.products_model.item(row, 0).text())
        product_name = self.products_model.item(row, 1).text()
        price = float(self.products_model.item(row, 3).text())
        quantity = self.quantitySpinBox.value()
        total_price = price * quantity

        # Проверка наличия товара на складе
        current_stock = self.get_product_stock(product_id)
        if quantity > current_stock:
            QMessageBox.warning(self, "Ошибка", f"Недостаточно товара на складе! В наличии: {current_stock} шт.")
            return

        # Добавление в корзину
        cart_item = {
            'id': product_id,
            'name': product_name,
            'price': price,
            'quantity': quantity,
            'total': total_price
        }

        # Проверяем, есть ли уже такой товар в корзине
        existing_item_index = -1
        for i, item in enumerate(self.cart_items):
            if item['id'] == product_id:
                existing_item_index = i
                break

        if existing_item_index >= 0:
            # Обновляем существующий товар
            self.cart_items[existing_item_index]['quantity'] += quantity
            self.cart_items[existing_item_index]['total'] += total_price
        else:
            # Добавляем новый товар
            self.cart_items.append(cart_item)

        # Уменьшаем количество на складе
        new_stock = current_stock - quantity
        self.update_product_stock(product_id, new_stock)

        self.update_cart_display()
        QMessageBox.information(self, "Успех", f"Товар '{product_name}' добавлен в корзину!")

    def remove_from_cart(self):
        """Удаление выбранного товара из корзины"""
        selection = self.cartTable.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите товар для удаления из корзины!")
            return

        row = selection[0].row()
        cart_item = self.cart_items[row]
        product_name = cart_item['name']
        product_id = cart_item['id']
        quantity = cart_item['quantity']

        # Возвращаем товар на склад
        current_stock = self.get_product_stock(product_id)
        new_stock = current_stock + quantity
        self.update_product_stock(product_id, new_stock)

        # Удаляем из списка
        self.cart_items.pop(row)
        self.update_cart_display()

        QMessageBox.information(self, "Успех", f"Товар '{product_name}' удален из корзины!")

    def clear_cart(self):
        """Очистка всей корзины"""
        if not self.cart_items:
            QMessageBox.information(self, "Информация", "Корзина уже пуста!")
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     "Вы уверены, что хотите очистить всю корзину?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Возвращаем все товары на склад
            for item in self.cart_items:
                current_stock = self.get_product_stock(item['id'])
                new_stock = current_stock + item['quantity']
                self.update_product_stock(item['id'], new_stock)

            self.cart_items.clear()
            self.update_cart_display()
            QMessageBox.information(self, "Успех", "Корзина очищена!")

    def update_cart_display(self):
        """Обновление отображения корзины и общей суммы"""
        self.cart_model.removeRows(0, self.cart_model.rowCount())
        self.total_amount = 0

        for item in self.cart_items:
            row_items = [
                QStandardItem(item['name']),
                QStandardItem(str(item['quantity'])),
                QStandardItem(f"{item['price']:,.2f} ₽"),
                QStandardItem(f"{item['total']:,.2f} ₽")
            ]

            # Выравнивание числовых колонок
            row_items[1].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_items[2].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.cart_model.appendRow(row_items)
            self.total_amount += item['total']

        # Обновление общей суммы
        self.totalLabel.setText(f"💰 Итого: {self.total_amount:,.2f} ₽")

    def create_sale(self):
        """Оформление продажи"""
        if not self.cart_items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста! Добавьте товары перед оформлением продажи.")
            return

        # Дополнительная проверка наличия товаров (на случай параллельных изменений)
        for item in self.cart_items:
            current_stock = self.get_product_stock(item['id'])
            if current_stock < 0:  # На случай если где-то была ошибка в логике
                QMessageBox.critical(self, "Ошибка",
                                     f"Недостаточно товара '{item['name']}' на складе! "
                                     f"Требуется: {item['quantity']}, в наличии: {current_stock}")
                return

        # Здесь должна быть логика сохранения продажи в базу данных
        # Пока просто показываем сообщение об успехе

        sale_details = "\n".join([f"- {item['name']} x{item['quantity']} = {item['total']:,.2f} ₽"
                                  for item in self.cart_items])

        QMessageBox.information(self, "Продажа оформлена!",
                                f"Продажа успешно оформлена!\n\n"
                                f"Состав заказа:\n{sale_details}\n\n"
                                f"Общая сумма: {self.total_amount:,.2f} ₽")

        # Очищаем корзину после успешной продажи
        # Товары уже списаны со склада при добавлении в корзину
        self.cart_items.clear()
        self.update_cart_display()

    def search_products(self):
        """Поиск товаров"""
        search_text = self.searchInput.text().strip().lower()

        if not search_text:
            # Показываем все товары если поиск пустой
            for row in range(self.products_model.rowCount()):
                self.productsTable.setRowHidden(row, False)
            return

        # Фильтрация товаров
        for row in range(self.products_model.rowCount()):
            product_name = self.products_model.item(row, 1).text().lower()
            product_article = self.products_model.item(row, 2).text().lower()

            if search_text in product_name or search_text in product_article:
                self.productsTable.setRowHidden(row, False)
            else:
                self.productsTable.setRowHidden(row, True)

    def show_filters(self):
        """Показ диалога фильтров"""
        QMessageBox.information(self, "Фильтры",
                                "Функция фильтров находится в разработке!")

    def switch_section(self, section_name):
        """Переключение между разделами приложения"""
        self.sectionTitle.setText(section_name)

        # Снимаем выделение с других кнопок навигации
        nav_buttons = [self.sales, self.storage, self.purchase]
        for button in nav_buttons:
            if button.text().find(section_name) == -1:
                button.setChecked(False)

        # Показываем сообщение о переключении
        if section_name != "Продажи":
            QMessageBox.information(self, "Переключение раздела",
                                    f"Раздел '{section_name}' находится в разработке!")


def main():
    app = QApplication(sys.argv)

    # Проверяем существование UI файла
    ui_file_path = os.path.join(os.path.dirname(__file__), "продажи — ко222пия.ui")
    if not os.path.exists(ui_file_path):
        print(f"Ошибка: UI файл не найден по пути: {ui_file_path}")
        return

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()