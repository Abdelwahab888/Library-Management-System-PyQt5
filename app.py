import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QLabel, QMessageBox)
from database import DatabaseHandler
from models import Book

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Smart Library Management System')
        self.setGeometry(100, 100, 600, 400)

        # Key elements
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Input boxes
        self.title_input = QLineEdit(); self.title_input.setPlaceholderText('Book Title')
        self.author_input = QLineEdit(); self.author_input.setPlaceholderText('Author')
        self.isbn_input = QLineEdit(); self.isbn_input.setPlaceholderText('ISBN')

        # Buttons
        self.add_btn = QPushButton('add book')
        self.add_btn.clicked.connect(self.add_book)
        
        self.delete_btn = QPushButton('Delete the selected book')
        self.delete_btn.setStyleSheet("background-color: #ff4444; color: white;")
        self.delete_btn.clicked.connect(self.delete_book)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'ISBN'])

        # --- Research Section ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('search with the book name or ISBN')
        self.search_btn = QPushButton('search:')
        self.search_btn.clicked.connect(self.search_books)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        self.layout.addLayout(search_layout)
        # -------------------------

        # Adding elements to the interface
        self.layout.addWidget(QLabel("add new book: "))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.author_input)
        self.layout.addWidget(self.isbn_input)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.delete_btn)

        self.central_widget.setLayout(self.layout)
        self.load_data()

    def load_data(self):
        all_books = self.db.get_all_books()
        self.display_books(all_books)

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()

        if title and author and isbn:
            new_book = Book(title, author, isbn)
            if self.db.add_book(new_book):
                self.load_data() # Table Update
                self.title_input.clear(); self.author_input.clear(); self.isbn_input.clear()
            else:
                QMessageBox.warning(self, "Error", "Add failed (Possibly duplicate ISBN)")
        else:
            QMessageBox.critical(self, "Alert", "Please fill in all boxes")
    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            book_id = self.table.item(selected_row, 0).text()
            self.db.delete_book(book_id)
            self.load_data()
        else:
            QMessageBox.warning(self, "Warning", "Choose a book from the table first")

    def search_books(self):
        keyword = self.search_input.text().lower()
        all_books = self.db.get_all_books() # We get the data in a List
        
        # Applying Data Structure (Filtering a List)
        filtered_books = [
            b for b in all_books 
            if keyword in b['title'].lower() or keyword in b['isbn']
        ]
        
        self.display_books(filtered_books)

    def display_books(self, books_list):
        # Helper function to display the filtered list in the table
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(books_list):
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_number, 1, QTableWidgetItem(row_data['title']))
            self.table.setItem(row_number, 2, QTableWidgetItem(row_data['author']))
            self.table.setItem(row_number, 3, QTableWidgetItem(row_data['isbn']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LibraryApp()
    ex.show()
    sys.exit(app.exec_())
