import sys, os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlQuery
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLabel, QSizePolicy, QPushButton, QComboBox, \
    QHBoxLayout, QTableView, QHeaderView, QVBoxLayout


class Movie_maker(QWidget):
    """
    Visualization of the information in the database in the form of a table.
    """
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setMinimumSize(1000, 600)
        self.setWindowTitle('Movies manager')
        self.createConnection()
        self.createTable()
        self.setupWidgets()
        self.show()

    def create_connection(self):
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("Movies.db")

        if not database.open():
            print("Unable to open data source file.")
            sys.exit(1)  # Error code 1 - signifies error

        # Check if tables we need exist in the database
        tables_needed = {'Movies'}
        tables_not_found = tables_needed - set(database.tables())

        if tables_not_found:
            QMessageBox.critical(None, "Error", f"The following tables are missing from the database: {tables_not_found}")
            sys.exit(1)

    def create_table(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = QSqlRelationalTableModel()
        self.model.setTable('Movies')
        self.model.setHeaderData(self.model.fieldIndex('id'), Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('movie_name'), Qt.Horizontal, "Movie name")
        self.model.setHeaderData(self.model.fieldIndex('genre'), Qt.Horizontal, "Genres")
        self.model.setHeaderData(self.model.fieldIndex('year'), Qt.Horizontal, "Year of release")
        self.model.setHeaderData(self.model.fieldIndex('rating'), Qt.Horizontal, "Rating")
        self.model.setHeaderData(self.model.fieldIndex('url_images'), Qt.Horizontal, "Poster")
        self.model.setHeaderData(self.model.fieldIndex('hours'), Qt.Horizontal, "Duration")
        self.model.setHeaderData(self.model.fieldIndex('director'), Qt.Horizontal, "Directors")
        self.model.setHeaderData(self.model.fieldIndex('actors'), Qt.Horizontal, "Actors")
        self.model.setHeaderData(self.model.fieldIndex('link'), Qt.Horizontal, "Link")
        # populate the model with data
        self.model.select()

    def setup_widgets(self):
        """
        Create instances of widgets, the table view and set layouts.
        """
        icons_path = "icons"

        title = QLabel("Movie Management System")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")

        add_product_button = QPushButton("Add Movie")
        add_product_button.setIcon(QIcon(os.path.join(icons_path, "plus.png")))
        add_product_button.setStyleSheet("padding: 10px")
        add_product_button.clicked.connect(self.addItem)

        del_product_button = QPushButton("Delete")
        del_product_button.setIcon(QIcon(os.path.join(icons_path, "trash_can.png")))
        del_product_button.setStyleSheet("padding: 10px")
        del_product_button.clicked.connect(self.deleteItem)

        # set up sorting combobox
        sorting_options = ["Sort by ID", "Sort by Movie name", "Sort by Genres",
                           "Sort by Year of release", "Sort by Rating", "Sort by Poster", "Sort by Duration",
                           "Sort by Directors", "Sort by Actors", "Sort by Link"]

        sort_name_cb = QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)

        buttons_h_box = QHBoxLayout()
        buttons_h_box.addWidget(add_product_button)
        buttons_h_box.addWidget(del_product_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_name_cb)

        # Widget to contain editing buttons
        edit_buttons = QWidget()
        edit_buttons.setLayout(buttons_h_box)

        # Create table view and set model
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        # Instantiate the delegate
        delegate = QSqlRelationalDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        # Main layout
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(title, Qt.AlignLeft)
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def add_item(self):
        """
        Add a new record to the last row of the table.
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM Movies")
        if query.next():
            print(query.value(0))
            id = int(query.value(0))

    def delete_item(self):
        """
        Delete an entire row from the table.
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()

    def set_sorting_order(self, text):
        """
        Sort the rows in table.
        """
        # mode = 0
        if text == "Sort by ID":
            self.model.setSort(self.model.fieldIndex('id'), Qt.AscendingOrder)
            # self.model.setSort(self.model.fieldIndex('id'), mode if Qt.DescendingOrder else Qt.AscendingOrder)
        elif text == "Sort by Movie name":
            self.model.setSort(self.model.fieldIndex('movie_name'), Qt.AscendingOrder)
        elif text == "Sort by Genres":
            self.model.setSort(self.model.fieldIndex('genre'), Qt.AscendingOrder)
        elif text == "Sort by Year of release":
            self.model.setSort(self.model.fieldIndex('year'), Qt.AscendingOrder)
        elif text == "Sort by Rating":
            self.model.setSort(self.model.fieldIndex('rating'), Qt.AscendingOrder)
        elif text == "Sort by Poster":
            self.model.setSort(self.model.fieldIndex('url_images'), Qt.AscendingOrder)
        elif text == "Sort by Duration":
            self.model.setSort(self.model.fieldIndex('hours'), Qt.AscendingOrder)
        elif text == "Sort by Directors":
            self.model.setSort(self.model.fieldIndex('director'), Qt.AscendingOrder)
        elif text == "Sort by Actors":
            self.model.setSort(self.model.fieldIndex('actors'), Qt.AscendingOrder)
        elif text == "Sort by Link":
            self.model.setSort(self.model.fieldIndex('link'), Qt.AscendingOrder)

        self.model.select()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Movie_maker()
    window.show()
    sys.exit(app.exec_())
