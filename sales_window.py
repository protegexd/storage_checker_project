import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QMessageBox)
from PyQt6.uic import loadUi


class SalesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('sales_window.ui', self)

        # Тестовые данные
        self.products = [
            {"name": "iPhone 15", "price": 99990, "stock": 10},
            {"name": "Samsung S24", "price": 89990, "stock": 8},
            {"name": "MacBook Air", "price": 129990, "stock": 5},
            {"name": "iPad", "price": 59990, "stock": 15},
        ]

        self.cart = []

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        # Заполняем таблицу товаров
        self.productsTable.setRowCount(len(self.products))
        for row, product in enumerate(self.products):
            self.productsTable.setItem(row, 0, QTableWidgetItem(product["name"]))
            self.productsTable.setItem(row, 1, QTableWidgetItem(str(product["price"])))
            self.productsTable.setItem(row, 2, QTableWidgetItem(str(product["stock"])))

    def connect_signals(self):
        self.searchButton.clicked.connect(self.search_products)
        self.addButton.clicked.connect(self.add_to_cart)
        self.removeButton.clicked.connect(self.remove_from_cart)
        self.clearButton.clicked.connect(self.clear_cart)
        self.checkoutButton.clicked.connect(self.checkout)

    def search_products(self):
        search_text = self.searchInput.text().lower()
        if not search_text:
            self.setup_ui()
            return

        for row in range(self.productsTable.rowCount()):
            item = self.productsTable.item(row, 0)
            if item and search_text in item.text().lower():
                self.productsTable.setRowHidden(row, False)
            else:
                self.productsTable.setRowHidden(row, True)

    def add_to_cart(self):
        current_row = self.productsTable.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return

        product_name = self.productsTable.item(current_row, 0).text()
        price = int(self.productsTable.item(current_row, 1).text())
        quantity = self.quantitySpin.value()

        # Проверяем наличие
        stock = int(self.productsTable.item(current_row, 2).text())
        if quantity > stock:
            QMessageBox.warning(self, "Ошибка", f"Недостаточно товара. В наличии: {stock}")
            return

        # Добавляем в корзину
        self.cart.append({
            "name": product_name,
            "price": price,
            "quantity": quantity
        })

        self.update_cart()
        QMessageBox.information(self, "Успех", f"Товар добавлен в корзину")

    def remove_from_cart(self):
        current_row = self.cartTable.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
            return

        self.cart.pop(current_row)
        self.update_cart()

    def clear_cart(self):
        self.cart.clear()
        self.update_cart()

    def update_cart(self):
        self.cartTable.setRowCount(len(self.cart))

        total = 0
        for row, item in enumerate(self.cart):
            self.cartTable.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.cartTable.setItem(row, 1, QTableWidgetItem(str(item["price"])))
            self.cartTable.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            subtotal = item["price"] * item["quantity"]
            self.cartTable.setItem(row, 3, QTableWidgetItem(str(subtotal)))
            total += subtotal

        self.totalLabel.setText(f"Итого: {total} руб")

    def checkout(self):
        if not self.cart:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста")
            return

        customer_name = self.customerInput.text().strip()
        if not customer_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя покупателя")
            return

        total = sum(item["price"] * item["quantity"] for item in self.cart)

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Продажа для: {customer_name}\nСумма: {total} руб\n\nПодтвердить?")

        if reply == QMessageBox.StandardButton.Yes:
            # Обновляем остатки
            for cart_item in self.cart:
                for product in self.products:
                    if product["name"] == cart_item["name"]:
                        product["stock"] -= cart_item["quantity"]

            self.cart.clear()
            self.update_cart()
            self.customerInput.clear()
            self.setup_ui()  # Обновляем таблицу товаров

            QMessageBox.information(self, "Успех", "Продажа оформлена!")


def main():
    app = QApplication(sys.argv)
    window = SalesWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()