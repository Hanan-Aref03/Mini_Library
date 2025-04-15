from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bookmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    checked_out = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'year': self.year,
            'checked_out': self.checked_out
        }

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return {'message': 'Book Manager API working!'}

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from fuzzywuzzy import fuzz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bookmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🧱 Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    checked_out = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'year': self.year,
            'checked_out': self.checked_out
        }

@app.before_first_request
def create_tables():
    db.create_all()

# 🔍 Home
@app.route('/')
def home():
    return jsonify({'message': 'Book Manager API is running!'})

# 📚 List All Books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# ➕ Add a Book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data.get('isbn'),
        genre=data.get('genre'),
        year=data.get('year'),
        checked_out=False
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

# ✏️ Update a Book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.genre = data.get('genre', book.genre)
    book.year = data.get('year', book.year)
    db.session.commit()
    return jsonify(book.to_dict())

# Delete a Book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

# 📥 Check-out a Book
@app.route('/books/<int:book_id>/checkout', methods=['POST'])
def checkout_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.checked_out:
        return jsonify({'message': 'Book is already checked out'}), 400
    book.checked_out = True
    db.session.commit()
    return jsonify({'message': 'Book checked out', 'book': book.to_dict()})

# 📤 Check-in a Book
@app.route('/books/<int:book_id>/checkin', methods=['POST'])
def checkin_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.checked_out:
        return jsonify({'message': 'Book is already checked in'}), 400
    book.checked_out = False
    db.session.commit()
    return jsonify({'message': 'Book checked in', 'book': book.to_dict()})

# 🔎 Search Books
@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    results = []
    for book in Book.query.all():
        if (
            fuzz.partial_ratio(query.lower(), book.title.lower()) > 70 or
            fuzz.partial_ratio(query.lower(), book.author.lower()) > 70 or
            (book.isbn and fuzz.partial_ratio(query.lower(), book.isbn.lower()) > 70) or
            (book.genre and fuzz.partial_ratio(query.lower(), book.genre.lower()) > 70)
        ):
            results.append(book.to_dict())
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)



