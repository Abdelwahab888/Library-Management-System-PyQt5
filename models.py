# models.py

class Book:
    def __init__(self, title, author, isbn, status="Available"):
        # Encapsulation: بنخلي البيانات Private باستخدام __
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__status = status

    # Getters عشان نقدر نقرأ البيانات من بره الكلاس
    def get_details(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "isbn": self.__isbn,
            "status": self.__status
        }

    # Setter عشان نحدث حالة الكتاب (مستعار أو متاح)
    def set_status(self, new_status):
        self.__status = new_status

    @property
    def isbn(self):
        return self.__isbn