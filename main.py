import sys
import csv
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QInputDialog, QVBoxLayout, QHeaderView,
                             QAbstractItemView, QDialog, QTabWidget,
                             QWidget, QHBoxLayout, QPushButton, QStackedWidget,
                             QTableView, QSpinBox, QLineEdit, QLabel, QGroupBox,
                             QFormLayout, QDateEdit, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDate
from PyQt6.QtGui import QColor, QPalette, QStandardItemModel, QStandardItem
from PyQt6 import uic
from interface import Ui_MainWindow


class DatabaseManager:
    def __init__(self, products_file="database.csv", sales_file="sales.csv", purchases_file="purchases.csv"):
        self.products_file = products_file
        self.sales_file = sales_file
        self.purchases_file = purchases_file
        self.data = {"products": [], "sales": [], "purchases": [], "last_id": 0, "last_sale_id": 0,
                     "last_purchase_id": 0}
        self.load_data()

    def load_data(self):
        """Загрузка данных из CSV файлов"""
        try:
            # Загрузка товаров
            if os.path.exists(self.products_file):
                with open(self.products_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.data["products"] = []
                    for row in reader:
                        # Преобразование числовых полей
                        row['id'] = int(row['id'])
                        row['quantity'] = int(row['quantity'])
                        row['price'] = int(row['price'])
                        self.data["products"].append(row)
                        # Обновление последнего ID
                        if row['id'] > self.data["last_id"]:
                            self.data["last_id"] = row['id']
                print(f"Товары загружены из {self.products_file}")
            else:
                self.save_products()
                print(f"Создан новый файл {self.products_file}")

            # Загрузка продаж
            if os.path.exists(self.sales_file):
                with open(self.sales_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.data["sales"] = []
                    for row in reader:
                        row['id'] = int(row['id'])
                        row['product_id'] = int(row['product_id'])
                        row['quantity'] = int(row['quantity'])
                        row['price'] = int(row['price'])
                        self.data["sales"].append(row)
                        if row['id'] > self.data["last_sale_id"]:
                            self.data["last_sale_id"] = row['id']
                print(f"Продажи загружены из {self.sales_file}")
            else:
                self.save_sales()
                print(f"Создан новый файл {self.sales_file}")

            # Загрузка закупок
            if os.path.exists(self.purchases_file):
                with open(self.purchases_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.data["purchases"] = []
                    for row in reader:
                        row['id'] = int(row['id'])
                        row['product_id'] = int(row['product_id'])
                        row['quantity'] = int(row['quantity'])
                        row['purchase_price'] = int(row['purchase_price'])
                        self.data["purchases"].append(row)
                        if row['id'] > self.data["last_purchase_id"]:
                            self.data["last_purchase_id"] = row['id']
                print(f"Закупки загружены из {self.purchases_file}")
            else:
                self.save_purchases()
                print(f"Создан новый файл {self.purchases_file}")

        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.save_data()

    def save_products(self):
        """Сохранение товаров в CSV"""
        try:
            with open(self.products_file, 'w', encoding='utf-8', newline='') as f:
                if self.data["products"]:
                    fieldnames = ['id', 'name', 'category', 'quantity', 'price', 'description']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data["products"])
            return True
        except Exception as e:
            print(f"Ошибка сохранения товаров: {e}")
            return False

    def save_sales(self):
        """Сохранение продаж в CSV"""
        try:
            with open(self.sales_file, 'w', encoding='utf-8', newline='') as f:
                if self.data["sales"]:
                    fieldnames = ['id', 'date', 'product_id', 'product_name', 'quantity', 'price', 'type']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data["sales"])
            return True
        except Exception as e:
            print(f"Ошибка сохранения продаж: {e}")
            return False

    def save_purchases(self):
        """Сохранение закупок в CSV"""
        try:
            with open(self.purchases_file, 'w', encoding='utf-8', newline='') as f:
                if self.data["purchases"]:
                    fieldnames = ['id', 'date', 'product_id', 'product_name', 'quantity', 'purchase_price', 'supplier']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data["purchases"])
            return True
        except Exception as e:
            print(f"Ошибка сохранения закупок: {e}")
            return False

    def save_data(self):
        """Сохранение всех данных"""
        success = True
        success = self.save_products() and success
        success = self.save_sales() and success
        success = self.save_purchases() and success

        if not success:
            QMessageBox.critical(None, "Ошибка", "Не удалось сохранить данные")
        return success

    def get_products(self):
        """Получить список товаров"""
        return self.data["products"]

    def get_sales(self):
        """Получить список продаж"""
        return self.data.get("sales", [])

    def get_purchases(self):
        """Получить список закупок"""
        return self.data.get("purchases", [])

    def get_next_id(self):
        """Получить следующий ID товара"""
        self.data["last_id"] += 1
        return self.data["last_id"]

    def get_next_sale_id(self):
        """Получить следующий ID продажи"""
        if "last_sale_id" not in self.data:
            self.data["last_sale_id"] = 0
        self.data["last_sale_id"] += 1
        return self.data["last_sale_id"]

    def get_next_purchase_id(self):
        """Получить следующий ID закупки"""
        if "last_purchase_id" not in self.data:
            self.data["last_purchase_id"] = 0
        self.data["last_purchase_id"] += 1
        return self.data["last_purchase_id"]

    def add_product(self, product):
        """Добавить товар"""
        product["id"] = self.get_next_id()
        self.data["products"].append(product)
        return self.save_products()

    def add_sale(self, sale_data):
        """Добавить продажу"""
        sale_data["id"] = self.get_next_sale_id()
        sale_data["date"] = datetime.now().isoformat()
        if "sales" not in self.data:
            self.data["sales"] = []
        self.data["sales"].append(sale_data)
        return self.save_sales()

    def add_purchase(self, purchase_data):
        """Добавить закупку"""
        purchase_data["id"] = self.get_next_purchase_id()
        purchase_data["date"] = datetime.now().isoformat()
        if "purchases" not in self.data:
            self.data["purchases"] = []
        self.data["purchases"].append(purchase_data)
        return self.save_purchases()

    def update_product(self, product_id, updated_data):
        """Обновить товар"""
        for product in self.data["products"]:
            if product["id"] == product_id:
                product.update(updated_data)
                return self.save_products()
        return False

    def delete_product(self, product_id):
        """Удалить товар"""
        self.data["products"] = [p for p in self.data["products"] if p["id"] != product_id]
        return self.save_products()

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


class SalesTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.sales = data if data else []
        self.headers = ['ID', 'Дата', 'Товар', 'Количество', 'Цена', 'Сумма', 'Тип']

    def rowCount(self, parent=QModelIndex()):
        return len(self.sales)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        sale = self.sales[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:  # ID
                return str(sale['id'])
            elif col == 1:  # Дата
                date_str = sale.get('date', '')
                try:
                    if 'T' in date_str:
                        dt = datetime.fromisoformat(date_str)
                        return dt.strftime("%d.%m.%Y %H:%M")
                except:
                    pass
                return date_str
            elif col == 2:  # Товар
                return sale['product_name']
            elif col == 3:  # Количество
                return str(sale['quantity'])
            elif col == 4:  # Цена
                return f"{sale['price']:,.0f} ₽"
            elif col == 5:  # Сумма
                total = sale['quantity'] * sale['price']
                return f"{total:,.0f} ₽"
            elif col == 6:  # Тип
                return sale.get('type', 'Продажа')

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [3, 4, 5]:  # Числовые колонки выравниваем по правому краю
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self.sales = new_data
        self.endResetModel()


class PurchasesTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.purchases = data if data else []
        self.headers = ['ID', 'Дата', 'Товар', 'Количество', 'Цена закупки', 'Сумма', 'Поставщик']

    def rowCount(self, parent=QModelIndex()):
        return len(self.purchases)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        purchase = self.purchases[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:  # ID
                return str(purchase['id'])
            elif col == 1:  # Дата
                date_str = purchase.get('date', '')
                try:
                    if 'T' in date_str:
                        dt = datetime.fromisoformat(date_str)
                        return dt.strftime("%d.%m.%Y %H:%M")
                except:
                    pass
                return date_str
            elif col == 2:  # Товар
                return purchase['product_name']
            elif col == 3:  # Количество
                return str(purchase['quantity'])
            elif col == 4:  # Цена закупки
                return f"{purchase['purchase_price']:,.0f} ₽"
            elif col == 5:  # Сумма
                total = purchase['quantity'] * purchase['purchase_price']
                return f"{total:,.0f} ₽"
            elif col == 6:  # Поставщик
                return purchase.get('supplier', 'Не указан')

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [3, 4, 5]:  # Числовые колонки выравниваем по правому краю
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self.purchases = new_data
        self.endResetModel()

class SalesWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.cart_items = []
        self.total_amount = 0

        # Создаем макет
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создаем и настраиваем элементы интерфейса вручную
        self.setup_ui(layout)

        # Настройка таблиц
        self.setup_tables()

        # Подключение сигналов
        self.connect_signals()

        # Загрузка данных
        self.load_products()

    def setup_ui(self, layout):
        """Создание интерфейса вручную"""
        # Панель управления с кнопками навигации
        nav_layout = QHBoxLayout()

        # Кнопка возврата на склад
        self.backButton = QPushButton("← Вернуться на склад")
        self.backButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)

        # Кнопка истории продаж
        self.historyButton = QPushButton("📊 История продаж")
        self.historyButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)

        nav_layout.addWidget(self.backButton)
        nav_layout.addStretch()
        nav_layout.addWidget(self.historyButton)
        layout.addLayout(nav_layout)

        # Заголовок раздела
        self.sectionTitle = QLabel("Продажи")
        self.sectionTitle.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.sectionTitle)

        # Панель поиска
        search_layout = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Поиск товаров по названию, категории...")
        self.searchInput.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        self.search_button = QPushButton("🔍 Найти")
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.filter = QPushButton("⚙️ Фильтры")
        self.filter.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)

        search_layout.addWidget(self.searchInput)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.filter)
        layout.addLayout(search_layout)

        # Основной контент
        content_layout = QHBoxLayout()

        # Группа товаров
        products_group = QGroupBox("📦 Товары")
        products_layout = QVBoxLayout()
        self.productsTable = QTableView()
        self.productsTable.setStyleSheet("""
            QTableView {
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                selection-background-color: #007bff;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        self.productsTable.setAlternatingRowColors(True)
        self.productsTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.productsTable.setSortingEnabled(True)

        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Количество:")
        self.quantitySpinBox = QSpinBox()
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(999)
        self.quantitySpinBox.setValue(1)
        self.quantitySpinBox.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)
        self.addButton = QPushButton("➕ Добавить в корзину")
        self.addButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantitySpinBox)
        quantity_layout.addStretch()
        quantity_layout.addWidget(self.addButton)

        products_layout.addWidget(self.productsTable)
        products_layout.addLayout(quantity_layout)
        products_group.setLayout(products_layout)

        # Группа корзины
        cart_group = QGroupBox("🛒 Корзина")
        cart_layout = QVBoxLayout()
        self.cartTable = QTableView()
        self.cartTable.setStyleSheet("""
            QTableView {
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                selection-background-color: #17a2b8;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        self.cartTable.setAlternatingRowColors(True)
        self.cartTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cartTable.setSortingEnabled(True)

        cart_actions_layout = QHBoxLayout()
        self.removeButton = QPushButton("🗑️ Удалить")
        self.removeButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.clearButton = QPushButton("🗑️ Очистить корзину")
        self.clearButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        self.totalLabel = QLabel("💰 Итого: 0 ₽")
        self.totalLabel.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #d32f2f;
            background-color: #ffebee; 
            padding: 8px 16px;
            border-radius: 4px; 
            border: 1px solid #f44336;
        """)
        self.totalLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cart_actions_layout.addWidget(self.removeButton)
        cart_actions_layout.addWidget(self.clearButton)
        cart_actions_layout.addStretch()
        cart_actions_layout.addWidget(self.totalLabel)

        cart_layout.addWidget(self.cartTable)
        cart_layout.addLayout(cart_actions_layout)
        cart_group.setLayout(cart_layout)

        # Добавляем группы в основной layout
        content_layout.addWidget(products_group)
        content_layout.addWidget(cart_group)
        layout.addLayout(content_layout)

        # Кнопка оформления продажи
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        self.createSaleButton = QPushButton("✅ Оформить продажу")
        self.createSaleButton.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        footer_layout.addWidget(self.createSaleButton)
        layout.addLayout(footer_layout)

    def setup_tables(self):
        """Настройка таблиц товаров и корзины"""
        # Таблица товаров
        self.products_model = QStandardItemModel()
        self.products_model.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Цена", "В наличии"])
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
        self.searchInput.returnPressed.connect(self.search_products)

        # Новые кнопки
        self.backButton.clicked.connect(self.return_to_storage)
        self.historyButton.clicked.connect(self.show_sales_history)

    def return_to_storage(self):
        """Вернуться на склад"""
        self.main_window.show_storage()

    def show_sales_history(self):
        """Показать историю продаж"""
        self.main_window.show_sales_history()

    def load_products(self):
        """Загрузка товаров из базы данных"""
        products = self.db.get_products()
        self.products_model.removeRows(0, self.products_model.rowCount())

        for product in products:
            items = [
                QStandardItem(str(product['id'])),
                QStandardItem(product['name']),
                QStandardItem(product['category']),
                QStandardItem(f"{product['price']:,.0f} ₽"),
                QStandardItem(str(product['quantity']))
            ]

            # Выравнивание числовых колонок по правому краю
            items[0].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[4].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.products_model.appendRow(items)

    def add_to_cart(self):
        """Добавление выбранного товара в корзину"""
        selection = self.productsTable.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите товар из списка!")
            return

        row = selection[0].row()
        product_id = int(self.products_model.item(row, 0).text())
        product_name = self.products_model.item(row, 1).text()
        price_text = self.products_model.item(row, 3).text().replace(' ₽', '').replace(',', '')
        price = float(price_text)
        quantity = self.quantitySpinBox.value()

        # Проверка наличия товара на складе
        stock = int(self.products_model.item(row, 4).text())
        if quantity > stock:
            QMessageBox.warning(self, "Ошибка", f"Недостаточно товара на складе! В наличии: {stock} шт.")
            return

        total_price = price * quantity

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

        self.update_cart_display()
        QMessageBox.information(self, "Успех", f"Товар '{product_name}' добавлен в корзину!")

    def remove_from_cart(self):
        """Удаление выбранного товара из корзины"""
        selection = self.cartTable.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите товар для удаления из корзины!")
            return

        row = selection[0].row()
        product_name = self.cart_model.item(row, 0).text()

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
                QStandardItem(f"{item['price']:,.0f} ₽"),
                QStandardItem(f"{item['total']:,.0f} ₽")
            ]

            # Выравнивание числовых колонок
            row_items[1].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_items[2].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.cart_model.appendRow(row_items)
            self.total_amount += item['total']

        # Обновление общей суммы
        self.totalLabel.setText(f"💰 Итого: {self.total_amount:,.0f} ₽")

    def create_sale(self):
        """Оформление продажи"""
        if not self.cart_items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста! Добавьте товары перед оформлением продажи.")
            return

        # Обновляем количество товаров в базе данных и сохраняем продажи
        for item in self.cart_items:
            # Находим товар в базе данных
            product = None
            for p in self.db.get_products():
                if p['id'] == item['id']:
                    product = p
                    break

            if product:
                new_quantity = product['quantity'] - item['quantity']
                if new_quantity < 0:
                    QMessageBox.warning(self, "Ошибка", f"Недостаточно товара '{product['name']}' на складе!")
                    return

                # Обновляем количество товара
                self.db.update_product(product['id'], {'quantity': new_quantity})

                # Сохраняем информацию о продаже
                sale_data = {
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'quantity': item['quantity'],
                    'price': product['price'],
                    'type': 'Продажа'
                }
                self.db.add_sale(sale_data)

        sale_details = "\n".join([f"- {item['name']} x{item['quantity']} = {item['total']:,.0f} ₽"
                                  for item in self.cart_items])

        QMessageBox.information(self, "Продажа оформлена!",
                                f"Продажа успешно оформлена!\n\n"
                                f"Состав заказа:\n{sale_details}\n\n"
                                f"Общая сумма: {self.total_amount:,.0f} ₽")

        # Очищаем корзину после успешной продажи
        self.cart_items.clear()
        self.update_cart_display()
        # Обновляем список товаров
        self.load_products()

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
            product_category = self.products_model.item(row, 2).text().lower()

            if search_text in product_name or search_text in product_category:
                self.productsTable.setRowHidden(row, False)
            else:
                self.productsTable.setRowHidden(row, True)

    def show_filters(self):
        """Показ диалога фильтров"""
        categories = list(set(p['category'] for p in self.db.get_products()))
        if not categories:
            QMessageBox.information(self, "Фильтры", "Нет категорий для фильтрации")
            return

        category, ok = QInputDialog.getItem(self, "Фильтр по категории",
                                            "Выберите категорию:", categories, 0, False)
        if ok and category:
            # Показываем только товары выбранной категории
            for row in range(self.products_model.rowCount()):
                product_category = self.products_model.item(row, 2).text()
                if product_category == category:
                    self.productsTable.setRowHidden(row, False)
                else:
                    self.productsTable.setRowHidden(row, True)


class PurchaseWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window

        # Создаем макет
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создаем и настраиваем элементы интерфейса
        self.setup_ui(layout)

        # Настройка таблиц
        self.setup_tables()

        # Подключение сигналов
        self.connect_signals()

        # Загрузка данных
        self.load_products()

    def setup_ui(self, layout):
        """Создание интерфейса закупок"""
        # Панель управления с кнопками навигации
        nav_layout = QHBoxLayout()

        # Кнопка возврата на склад
        self.backButton = QPushButton("← Вернуться на склад")
        self.backButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)

        # Кнопка истории закупок
        self.historyButton = QPushButton("📋 История закупок")
        self.historyButton.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)

        nav_layout.addWidget(self.backButton)
        nav_layout.addStretch()
        nav_layout.addWidget(self.historyButton)
        layout.addLayout(nav_layout)

        # Заголовок раздела
        self.sectionTitle = QLabel("Закупки товаров")
        self.sectionTitle.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.sectionTitle)

        # Основной контент
        content_layout = QHBoxLayout()

        # Группа товаров
        products_group = QGroupBox("📦 Товары на складе")
        products_layout = QVBoxLayout()
        self.productsTable = QTableView()
        self.productsTable.setStyleSheet("""
            QTableView {
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                selection-background-color: #007bff;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        self.productsTable.setAlternatingRowColors(True)
        self.productsTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.productsTable.setSortingEnabled(True)

        products_layout.addWidget(self.productsTable)
        products_group.setLayout(products_layout)

        # Группа формы закупки
        purchase_group = QGroupBox("🛒 Оформление закупки")
        purchase_layout = QVBoxLayout()

        # Форма закупки
        form_layout = QFormLayout()

        self.productCombo = QComboBox()
        self.productCombo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)

        self.quantitySpinBox = QSpinBox()
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(10000)
        self.quantitySpinBox.setValue(1)
        self.quantitySpinBox.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)

        self.purchasePriceSpinBox = QSpinBox()
        self.purchasePriceSpinBox.setMinimum(1)
        self.purchasePriceSpinBox.setMaximum(1000000)
        self.purchasePriceSpinBox.setValue(100)
        self.purchasePriceSpinBox.setPrefix("₽ ")
        self.purchasePriceSpinBox.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)

        self.supplierInput = QLineEdit()
        self.supplierInput.setPlaceholderText("Введите название поставщика")
        self.supplierInput.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)

        form_layout.addRow("Товар:", self.productCombo)
        form_layout.addRow("Количество:", self.quantitySpinBox)
        form_layout.addRow("Цена закупки:", self.purchasePriceSpinBox)
        form_layout.addRow("Поставщик:", self.supplierInput)

        purchase_layout.addLayout(form_layout)

        # Кнопка оформления закупки
        self.createPurchaseButton = QPushButton("✅ Оформить закупку")
        self.createPurchaseButton.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        purchase_layout.addWidget(self.createPurchaseButton)

        purchase_group.setLayout(purchase_layout)

        # Добавляем группы в основной layout
        content_layout.addWidget(products_group, 2)
        content_layout.addWidget(purchase_group, 1)
        layout.addLayout(content_layout)

    def setup_tables(self):
        """Настройка таблицы товаров"""
        # Таблица товаров
        self.products_model = QStandardItemModel()
        self.products_model.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Цена продажи", "В наличии"])
        self.productsTable.setModel(self.products_model)
        self.productsTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Настройка ширины колонок для таблицы товаров
        header = self.productsTable.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def connect_signals(self):
        """Подключение сигналов кнопок"""
        self.createPurchaseButton.clicked.connect(self.create_purchase)
        self.backButton.clicked.connect(self.return_to_storage)
        self.historyButton.clicked.connect(self.show_purchase_history)
        self.productsTable.selectionModel().selectionChanged.connect(self.on_product_selected)

    def return_to_storage(self):
        """Вернуться на склад"""
        self.main_window.show_storage()

    def show_purchase_history(self):
        """Показать историю закупок"""
        self.main_window.show_purchase_history()

    def on_product_selected(self):
        """Обработка выбора товара в таблице"""
        selection = self.productsTable.selectionModel().selectedRows()
        if selection:
            row = selection[0].row()
            product_id = int(self.products_model.item(row, 0).text())
            product_name = self.products_model.item(row, 1).text()

            # Устанавливаем выбранный товар в комбобокс
            index = self.productCombo.findData(product_id)
            if index >= 0:
                self.productCombo.setCurrentIndex(index)

    def load_products(self):
        """Загрузка товаров из базы данных"""
        products = self.db.get_products()

        # Очищаем таблицу
        self.products_model.removeRows(0, self.products_model.rowCount())

        # Очищаем комбобокс
        self.productCombo.clear()

        for product in products:
            # Добавляем в таблицу
            items = [
                QStandardItem(str(product['id'])),
                QStandardItem(product['name']),
                QStandardItem(product['category']),
                QStandardItem(f"{product['price']:,.0f} ₽"),
                QStandardItem(str(product['quantity']))
            ]

            # Выравнивание числовых колонок по правому краю
            items[0].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items[4].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.products_model.appendRow(items)

            # Добавляем в комбобокс
            self.productCombo.addItem(f"{product['name']} ({product['category']})", product['id'])

    def create_purchase(self):
        """Оформление закупки"""
        if self.productCombo.currentIndex() == -1:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите товар!")
            return

        product_id = self.productCombo.currentData()
        quantity = self.quantitySpinBox.value()
        purchase_price = self.purchasePriceSpinBox.value()
        supplier = self.supplierInput.text().strip()

        if not supplier:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, укажите поставщика!")
            return

        # Находим товар в базе данных
        product = None
        for p in self.db.get_products():
            if p['id'] == product_id:
                product = p
                break

        if product:
            # Обновляем количество товара
            new_quantity = product['quantity'] + quantity
            if self.db.update_product(product_id, {'quantity': new_quantity}):
                # Сохраняем информацию о закупке
                purchase_data = {
                    'product_id': product_id,
                    'product_name': product['name'],
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'supplier': supplier
                }

                if self.db.add_purchase(purchase_data):
                    # Обновляем отображение
                    self.load_products()

                    total_cost = quantity * purchase_price
                    QMessageBox.information(self, "Закупка оформлена!",
                                            f"Закупка успешно оформлена!\n\n"
                                            f"Товар: {product['name']}\n"
                                            f"Количество: {quantity} шт.\n"
                                            f"Цена закупки: {purchase_price:,.0f} ₽\n"
                                            f"Общая стоимость: {total_cost:,.0f} ₽\n"
                                            f"Поставщик: {supplier}")

                    # Очищаем форму
                    self.quantitySpinBox.setValue(1)
                    self.purchasePriceSpinBox.setValue(100)
                    self.supplierInput.clear()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось сохранить информацию о закупке")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить количество товара")
        else:
            QMessageBox.critical(self, "Ошибка", "Товар не найден в базе данных")


from PyQt6.QtWidgets import QFileDialog  # Добавьте этот импорт если его нет


class SalesHistoryDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("История продаж")
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("История продаж и списаний")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        # Статистика
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14px; margin: 5px;")
        layout.addWidget(self.stats_label)

        # Создаем таблицу для отображения продаж
        self.sales_table = QTableView()
        self.sales_model = SalesTableModel()
        self.sales_table.setModel(self.sales_model)

        # Настраиваем таблицу
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setSortingEnabled(True)

        # Настраиваем ширину колонок
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Дата
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Товар
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Количество
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Цена
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Сумма
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Тип

        layout.addWidget(self.sales_table)

        # Кнопки управления
        button_layout = QHBoxLayout()

        # Кнопка сохранения
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_btn.clicked.connect(self.save_data)

        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        refresh_btn.clicked.connect(self.load_sales)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_sales()

    def load_sales(self):
        """Загрузка истории продаж"""
        sales = self.db.get_sales()
        self.sales_model.update_data(sales)

        # Обновляем статистику
        total_sales = len(sales)
        total_amount = sum(sale['quantity'] * sale['price'] for sale in sales)
        self.stats_label.setText(f"Всего операций: {total_sales} | Общая сумма: {total_amount:,.0f} ₽")

    def save_data(self):
        """Сохранение истории продаж в файл"""
        sales = self.db.get_sales()

        if not sales:
            QMessageBox.warning(self, "Внимание", "Нет данных для сохранения!")
            return

        # Открываем диалог выбора файла с двумя форматами
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить историю продаж",
            f"история_продаж_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "CSV файлы (*.csv);;Текстовые файлы (*.txt)"
        )

        if not file_path:
            return  # Пользователь отменил

        try:
            if file_path.endswith('.csv'):
                self.save_to_csv(file_path, sales)
            else:
                self.save_to_txt(file_path, sales)

            QMessageBox.information(self, "Успех", f"Данные сохранены в:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def save_to_csv(self, file_path, sales):
        """Сохранение в CSV формат"""
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['ID', 'Дата', 'ID товара', 'Товар', 'Количество', 'Цена', 'Сумма', 'Тип']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for sale in sales:
                total = sale['quantity'] * sale['price']
                writer.writerow({
                    'ID': sale['id'],
                    'Дата': self.format_date(sale.get('date', '')),
                    'ID товара': sale['product_id'],
                    'Товар': sale['product_name'],
                    'Количество': sale['quantity'],
                    'Цена': f"{sale['price']:,.0f}",
                    'Сумма': f"{total:,.0f}",
                    'Тип': sale.get('type', 'Продажа')
                })

    def save_to_txt(self, file_path, sales):
        """Сохранение в TXT формат"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ИСТОРИЯ ПРОДАЖ\n")
            f.write("=" * 60 + "\n\n")

            for sale in sales:
                total = sale['quantity'] * sale['price']
                f.write(f"Дата: {self.format_date(sale.get('date', ''))}\n")
                f.write(f"Товар: {sale['product_name']}\n")
                f.write(f"Количество: {sale['quantity']} шт.\n")
                f.write(f"Цена: {sale['price']:,.0f} ₽\n")
                f.write(f"Сумма: {total:,.0f} ₽\n")
                f.write(f"Тип: {sale.get('type', 'Продажа')}\n")
                f.write("-" * 40 + "\n")

    def format_date(self, date_str):
        """Форматирование даты"""
        try:
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str)
                return dt.strftime("%d.%m.%Y %H:%M")
            return date_str
        except:
            return date_str

        
class PurchaseHistoryDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("История закупок")
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("История закупок")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        # Статистика
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14px; margin: 5px;")
        layout.addWidget(self.stats_label)

        # Создаем таблицу для отображения закупок
        self.purchases_table = QTableView()
        self.purchases_model = PurchasesTableModel()
        self.purchases_table.setModel(self.purchases_model)

        # Настраиваем таблицу
        self.purchases_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.purchases_table.setAlternatingRowColors(True)
        self.purchases_table.setSortingEnabled(True)

        # Настраиваем ширину колонок
        header = self.purchases_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Дата
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Товар
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Количество
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Цена закупки
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Сумма
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Поставщик

        layout.addWidget(self.purchases_table)

        # Кнопки управления
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        refresh_btn.clicked.connect(self.load_purchases)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_purchases()

    def load_purchases(self):
        """Загрузка истории закупок"""
        purchases = self.db.get_purchases()
        self.purchases_model.update_data(purchases)

        # Обновляем статистику
        total_purchases = len(purchases)
        total_quantity = sum(purchase['quantity'] for purchase in purchases)
        total_amount = sum(purchase['quantity'] * purchase['purchase_price'] for purchase in purchases)
        self.stats_label.setText(
            f"Всего закупок: {total_purchases} | Товаров: {total_quantity} шт. | Общая сумма: {total_amount:,.0f} ₽")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных
        self.db = DatabaseManager()

        # Инициализация UI из сгенерированного файла
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Настройка приложения
        self.setWindowTitle("Учет товаров магазина - v4.0 [Полная версия]")
        self.setMinimumSize(800, 600)

        # Настройка светлой цветовой палитры
        self.set_light_theme()

        # Создаем stacked widget для переключения между интерфейсами
        self.setup_stacked_widget()

        # Инициализация данных
        self.init_data()

        # Настройка таблицы
        self.setup_table()

        # Подключение сигналов
        self.connect_signals()

    def setup_stacked_widget(self):
        """Настройка stacked widget для переключения между интерфейсами"""
        # Создаем stacked widget
        self.stacked_widget = QStackedWidget()

        # Создаем виджеты для разных разделов
        self.sales_widget = SalesWidget(self.db, self)
        self.purchase_widget = PurchaseWidget(self.db, self)

        # Добавляем виджеты в stacked widget
        self.stacked_widget.addWidget(self.ui.centralwidget)  # индекс 0 - основной интерфейс (склад)
        self.stacked_widget.addWidget(self.sales_widget)  # индекс 1 - интерфейс продаж
        self.stacked_widget.addWidget(self.purchase_widget)  # индекс 2 - интерфейс закупок

        # Устанавливаем stacked widget как центральный виджет
        self.setCentralWidget(self.stacked_widget)

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
        self.stacked_widget.setCurrentIndex(0)
        self.ui.sectionTitle.setText("Склад товаров")
        self.update_navigation_style("storage")
        self.products = self.db.get_products()  # Загружаем все товары
        self.update_display()

    def show_purchase(self):
        """Показать раздел Закупка"""
        self.stacked_widget.setCurrentIndex(2)
        self.update_navigation_style("purchase")
        # Обновляем данные в виджете закупок
        self.purchase_widget.load_products()

    def show_sales(self):
        """Показать раздел Продажи"""
        self.stacked_widget.setCurrentIndex(1)
        self.update_navigation_style("sales")
        # Обновляем данные в виджете продаж
        self.sales_widget.load_products()

    def show_sales_history(self):
        """Показать историю продаж"""
        dialog = SalesHistoryDialog(self.db, self)
        dialog.exec()

    def show_purchase_history(self):
        """Показать историю закупок"""
        dialog = PurchaseHistoryDialog(self.db, self)
        dialog.exec()

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
                # Сохраняем информацию о продаже
                sale_data = {
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'quantity': quantity,
                    'price': product['price'],
                    'type': 'Продажа'
                }

                if self.db.add_sale(sale_data):
                    self.products = self.db.get_products()
                    total = quantity * product['price']
                    self.update_display()
                    QMessageBox.information(self, "Продажа создана",
                                            f"Продано {quantity} шт. товара '{product['name']}'\n"
                                            f"На сумму: {total:,.0f} ₽")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось сохранить информацию о продаже")
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
            if product['quantity'] > 0:
                # Сохраняем информацию о списании
                sale_data = {
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'quantity': product['quantity'],
                    'price': product['price'],
                    'type': f'Списание: {reason}'
                }

                if self.db.add_sale(sale_data):
                    if self.db.update_product(product['id'], {'quantity': 0}):
                        self.products = self.db.get_products()
                        self.update_display()
                        QMessageBox.information(self, "Списание",
                                                f"Товар '{product['name']}' списан по причине: {reason}\n"
                                                f"Списано {product['quantity']} шт.")
                    else:
                        QMessageBox.critical(self, "Ошибка", "Не удалось списать товар")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось сохранить информацию о списании")
            else:
                QMessageBox.information(self, "Списание", "Товар уже отсутствует на складе")

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