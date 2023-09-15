"""Michael Coughlin
9/15/2023
First API is a program that communicates with a database via the created API
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
app = Flask(__name__)

#Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.author}"

#server home message
@app.route('/')
def index():
    return 'Hello!'

#server book page
@app.route('/books')
#query database for all books
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'book name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return [{"books": output}]


@app.route('/books/<id>')
#find book by id
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"book name": book.book_name, "author": book.author, "publisher": book.publisher}


@app.route('/books', methods=['POST'])
#adds a book to the database
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return{'id': book.id}


@app.route('/books/<id>', methods=['DELETE'])
#deletes book from database
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()

