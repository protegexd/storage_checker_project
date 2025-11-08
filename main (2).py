import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QInputDialog, QVBoxLayout, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor, QPalette
from interface import Ui_MainWindow


class DatabaseManager:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = {"products": [], "last_id": 0}
        self.load_data()

    def load_data(self):
        """Загрузка данных из файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"Данные загружены из {self.filename}")
            else:
                self.save_data()  # Создаем файл с начальными данными
                print(f"Создан новый файл {self.filename}")
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.save_data()

    def save_data(self):
        """Сохранение данных в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в {self.filename}")
            return True
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
            QMessageBox.critical(None, "Ошибка", f"Не удалось сохранить данные: {e}")
            return False

    def get_products(self):
        """Получить список товаров"""
        return self.data["products"]

    def get_next_id(self):
        """Получить следующий ID"""
        self.data["last_id"] += 1
        return self.data["last_id"]

    def add_product(self, product):
        """Добавить товар"""
        product["id"] = self.get_next_id()
        self.data["products"].append(product)
        return self.save_data()

    def update_product(self, product_id, updated_data):
        """Обновить товар"""
        for product in self.data["products"]:
            if product["id"] == product_id:
                product.update(updated_data)
                return self.save_data()
        return False

    def delete_product(self, product_id):
        """Удалить товар"""
        self.data["products"] = [p for p in self.data["products"] if p["id"] != product_id]
        return self.save_data()

    def search_products(self, search_text):
        """Поиск товаров"""
        search_text = search_text.lower()
        return [
            p for p in self.data["products"]
            if (search_text in p["name"].lower() or
                search_text in p["category"].lower() or
                search_text in p.get("description", "").lower())
        ]

    def filter_by_category(self, category):
        """Фильтр по категории"""
        return [p for p in self.data["products"] if p["category"] == category]


class ProductTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.products = data if data else []
        self.headers = ['ID', 'Название', 'Категория', 'Количество', 'Цена', 'Сумма', 'Описание']

    def rowCount(self, parent=QModelIndex()):
        return len(self.products)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        product = self.products[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:  # ID
                return str(product['id'])
            elif col == 1:  # Название
                return product['name']
            elif col == 2:  # Категория
                return product['category']
            elif col == 3:  # Количество
                return str(product['quantity'])
            elif col == 4:  # Цена
                return f"{product['price']:,.0f} ₽"
            elif col == 5:  # Сумма
                total = product['quantity'] * product['price']
                return f"{total:,.0f} ₽"
            elif col == 6:  # Описание
                return product.get('description', '')

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [3, 4, 5]:  # Числовые колонки выравниваем по правому краю
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        elif role == Qt.ItemDataRole.BackgroundRole:
            # Подсветка товаров с малым количеством
            if product['quantity'] < 5:
                return QColor(255, 243, 205)  # Светло-желтый
            # Подсветка товаров с нулевым количеством
            elif product['quantity'] == 0:
                return QColor(248, 215, 218)  # Светло-красный

        elif role == Qt.ItemDataRole.ToolTipRole:
            # Всплывающая подсказка с полной информацией
            desc = product.get('description', 'Нет описания')
            return f"{product['name']}\nКатегория: {product['category']}\nОписание: {desc}"

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self.products = new_data
        self.endResetModel()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных
        self.db = DatabaseManager()

        # Инициализация UI из сгенерированного файла
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Настройка приложения
        self.setWindowTitle("Учет товаров магазина - v2.0 [База данных]")
        self.setMinimumSize(800, 600)

        # Настройка светлой цветовой палитры
        self.set_light_theme()

        # Инициализация данных
        self.init_data()

        # Настройка таблицы
        self.setup_table()

        # Подключение сигналов
        self.connect_signals()

    def set_light_theme(self):
        """Установка светлой темы для приложения"""
        app = QApplication.instance()
        
        # Создаем светлую палитру
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
        
        # Устанавливаем стиль, который хорошо работает на всех платформах
        app.setStyle('Fusion')

    def setup_table(self):
        """Настройка таблицы товаров"""
        # Создаем модель данных
        self.table_model = ProductTableModel(self.products)
        self.ui.tableView.setModel(self.table_model)

        # Настраиваем внешний вид таблицы
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setSortingEnabled(True)

        # Настраиваем ширину колонок
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Название
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Категория
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Количество
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Цена
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Сумма
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Описание

    def connect_signals(self):
        """Подключение всех сигналов к слотам"""
        # Навигационные кнопки
        self.ui.storage.clicked.connect(self.show_storage)
        self.ui.purchase.clicked.connect(self.show_purchase)
        self.ui.sales.clicked.connect(self.show_sales)

        # Кнопки управления товарами
        self.ui.add.clicked.connect(self.add_product)
        self.ui.edit.clicked.connect(self.edit_product)
        self.ui.delete_2.clicked.connect(self.delete_product)
        self.ui.copy.clicked.connect(self.copy_product)

        # Операционные кнопки
        self.ui.new_sale.clicked.connect(self.create_sale)
        self.ui.pushButton.clicked.connect(self.write_off_product)

        # Поиск и фильтры
        self.ui.search_button.clicked.connect(self.search_products)
        self.ui.searchInput.returnPressed.connect(self.search_products)
        self.ui.filter.clicked.connect(self.show_filters)

        # Двойной клик по таблице для редактирования
        self.ui.tableView.doubleClicked.connect(self.on_table_double_click)

    def init_data(self):
        """Инициализация данных из базы"""
        self.products = self.db.get_products()
        self.update_display()

    def update_display(self):
        """Обновление отображения данных"""
        total_products = len(self.products)
        total_value = sum(p["quantity"] * p["price"] for p in self.products)

        # Обновление статистики
        self.ui.statsLabel.setText(f"Всего: {total_products} товаров | Сумма: {total_value:,.0f} ₽")

        # Обновление данных в таблице
        if hasattr(self, 'table_model'):
            self.table_model.update_data(self.products)

    def get_selected_product(self):
        """Получить выбранный товар из таблицы"""
        selection = self.ui.tableView.selectionModel()
        if selection.hasSelection():
            row = selection.selectedRows()[0].row()
            if row < len(self.products):
                return self.products[row]
        return None

    def on_table_double_click(self, index):
        """Обработка двойного клика по таблице"""
        product = self.get_selected_product()
        if product:
            self.edit_selected_product()

    def show_storage(self):
        """Показать раздел Склад"""
        self.ui.sectionTitle.setText("Склад товаров")
        self.update_navigation_style("storage")
        self.products = self.db.get_products()  # Загружаем все товары
        self.update_display()

    def show_purchase(self):
        """Показать раздел Закупка"""
        self.ui.sectionTitle.setText("Закупка товаров")
        self.update_navigation_style("purchase")

    def show_sales(self):
        """Показать раздел Продажи"""
        self.ui.sectionTitle.setText("Продажи")
        self.update_navigation_style("sales")

    def update_navigation_style(self, active_button):
        """Обновление стиля навигационных кнопок"""
        buttons = {
            "storage": self.ui.storage,
            "purchase": self.ui.purchase,
            "sales": self.ui.sales
        }

        for name, button in buttons.items():
            if name == active_button:
                button.setChecked(True)
                button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 12px 15px;
                        border: none;
                        background-color: #007bff;
                        color: white;
                        border-left: 3px solid #0056b3;
                    }
                """)
            else:
                button.setChecked(False)
                button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 12px 15px;
                        border: none;
                        border-left: 3px solid transparent;
                        background-color: transparent;
                        color: #2c3e50;
                    }
                    QPushButton:hover {
                        background-color: #e9ecef;
                    }
                """)

    def add_product(self):
        """Добавить новый товар"""
        name, ok = QInputDialog.getText(self, "Добавить товар", "Название товара:")
        if ok and name:
            # Запрашиваем остальные данные
            category, ok1 = QInputDialog.getText(self, "Добавить товар", "Категория:")
            quantity, ok2 = QInputDialog.getInt(self, "Добавить товар", "Количество:", 0, 0, 10000)
            price, ok3 = QInputDialog.getInt(self, "Добавить товар", "Цена:", 0, 0, 1000000)
            description, ok4 = QInputDialog.getText(self, "Добавить товар", "Описание:")

            if ok1 and ok2 and ok3:
                new_product = {
                    "name": name,
                    "category": category,
                    "quantity": quantity,
                    "price": price,
                    "description": description if ok4 else ""
                }

                if self.db.add_product(new_product):
                    self.products = self.db.get_products()
                    self.update_display()
                    QMessageBox.information(self, "Успех", f"Товар '{name}' добавлен!")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось сохранить товар в базу данных")

    def edit_product(self):
        """Редактировать товар"""
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Внимание", "Выберите товар для редактирования")
            return

        self.edit_selected_product()

    def edit_selected_product(self):
        """Редактировать выбранный товар"""
        product = self.get_selected_product()
        if not product:
            return

        # Запрашиваем новые данные
        name, ok = QInputDialog.getText(self, "Редактировать товар", "Название:", text=product['name'])
        if ok:
            category, ok1 = QInputDialog.getText(self, "Редактировать товар", "Категория:", text=product['category'])
            quantity, ok2 = QInputDialog.getInt(self, "Редактировать товар", "Количество:", product['quantity'], 0,
                                                10000)
            price, ok3 = QInputDialog.getInt(self, "Редактировать товар", "Цена:", product['price'], 0, 1000000)
            description, ok4 = QInputDialog.getText(self, "Редактировать товар", "Описание:",
                                                    text=product.get('description', ''))

            if ok1 and ok2 and ok3:
                updated_data = {
                    'name': name,
                    'category': category,
                    'quantity': quantity,
                    'price': price,
                    'description': description if ok4 else product.get('description', '')
                }

                if self.db.update_product(product['id'], updated_data):
                    self.products = self.db.get_products()
                    self.update_display()
                    QMessageBox.information(self, "Успех", f"Товар '{name}' обновлен!")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить товар в базе данных")

    def delete_product(self):
        """Удалить товар"""
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления")
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Вы уверены, что хотите удалить товар '{product['name']}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_product(product['id']):
                self.products = self.db.get_products()
                self.update_display()
                QMessageBox.information(self, "Успех", f"Товар '{product['name']}' удален!")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить товар из базы данных")

    def copy_product(self):
        """Копировать товар"""
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Внимание", "Выберите товар для копирования")
            return

        new_product = product.copy()
        new_product['name'] = f"{product['name']} (копия)"
        # ID будет сгенерирован автоматически при добавлении

        if self.db.add_product(new_product):
            self.products = self.db.get_products()
            self.update_display()
            QMessageBox.information(self, "Успех", f"Товар скопирован!")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось скопировать товар в базу данных")

    def create_sale(self):
        """Создать продажу"""
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Внимание", "Выберите товар для продажи")
            return

        if product['quantity'] == 0:
            QMessageBox.warning(self, "Внимание", "Товар отсутствует на складе")
            return

        quantity, ok = QInputDialog.getInt(self, "Продажа товара",
                                           f"Количество для продажи (доступно: {product['quantity']}):",
                                           1, 1, product['quantity'])
        if ok:
            new_quantity = product['quantity'] - quantity
            if self.db.update_product(product['id'], {'quantity': new_quantity}):
                self.products = self.db.get_products()
                total = quantity * product['price']
                self.update_display()
                QMessageBox.information(self, "Продажа создана",
                                        f"Продано {quantity} шт. товара '{product['name']}'\n"
                                        f"На сумму: {total:,.0f} ₽")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить количество товара")

    def write_off_product(self):
        """Списать товар"""
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Внимание", "Выберите товар для списания")
            return

        reason, ok = QInputDialog.getText(self, "Списание товара", "Причина списания:")
        if ok and reason:
            if self.db.update_product(product['id'], {'quantity': 0}):
                self.products = self.db.get_products()
                self.update_display()
                QMessageBox.information(self, "Списание", f"Товар '{product['name']}' списан по причине: {reason}")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось списать товар")

    def search_products(self):
        """Поиск товаров"""
        search_text = self.ui.searchInput.text().strip()
        if search_text:
            # Используем метод поиска из базы данных
            filtered_products = self.db.search_products(search_text)
            self.table_model.update_data(filtered_products)
            self.ui.statsLabel.setText(f"Найдено: {len(filtered_products)} товаров")
        else:
            # Показываем все товары
            self.products = self.db.get_products()
            self.update_display()

    def show_filters(self):
        """Показать фильтры"""
        categories = list(set(p['category'] for p in self.db.get_products()))
        if not categories:
            QMessageBox.information(self, "Фильтры", "Нет категорий для фильтрации")
            return

        category, ok = QInputDialog.getItem(self, "Фильтр по категории",
                                            "Выберите категорию:", categories, 0, False)
        if ok and category:
            filtered_products = self.db.filter_by_category(category)
            self.table_model.update_data(filtered_products)
            self.ui.statsLabel.setText(f"Категория: {category} | Товаров: {len(filtered_products)}")

    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        # Автоматическое сохранение при закрытии
        if self.db.save_data():
            print("Данные сохранены при закрытии приложения")
        event.accept()


def main():
    # Создание приложения
    app = QApplication(sys.argv)

    # Создание и отображение главного окна
    window = MainWindow()
    window.show()

    # Запуск главного цикла
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
