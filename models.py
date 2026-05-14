# models.py

class Book:
    def __init__(self, title, author, isbn, status="Available"):
        # Encapsulation: We make the data private using __
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__status = status

    #Getters so we can read the data from outside the class
    def get_details(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "isbn": self.__isbn,
            "status": self.__status
        }

    # Setter to update the book's status (borrowed or available)
    def set_status(self, new_status):
        self.__status = new_status

    @property
    def isbn(self):
        return self.__isbn
