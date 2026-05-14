# database.py (نسخة SQLite - الأضمن للتسليم)
import sqlite3
import os

class DatabaseHandler:
    def __init__(self):
        # السطر ده هيعرفنا البرنامج شايف الفولدر فين بالظبط
        db_path = os.path.join(os.getcwd(), 'library.db')
        print(f"Warning: The database is located here: {db_path}")
        
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'Available'
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_book(self, book_obj):
        details = book_obj.get_details()
        query = "INSERT INTO books (title, author, isbn, status) VALUES (?, ?, ?, ?)"
        values = (details['title'], details['author'], details['isbn'], details['status'])
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        # تحويل النتائج لقائمة قواميس عشان تناسب الكود بتاعنا
        return [dict(row) for row in rows]

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(query, (book_id,))
        self.connection.commit()