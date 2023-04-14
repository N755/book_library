from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, IntegerField, validators
import csv
import json

app = Flask(__name__)
app.secret_key = 'secret'

class BookForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=50)])
    author = StringField('Author', [validators.Length(min=1, max=50)])
    publisher = StringField('Publisher', [validators.Length(min=1, max=50)])
    year = IntegerField('Year of publication', [validators.NumberRange(min=1000, max=9999)])
    pages = IntegerField('Number of pages', [validators.NumberRange(min=1)])

def save_book_to_csv(book):
    with open('books.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'author', 'publisher', 'year', 'pages']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        books = get_books_from_csv()

        if not books:
            book['id'] = 0
        else:
            max_id = max([int(book.get('id', 0)) for book in books])
            book['id'] = max_id + 1

        writer.writerow({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'publisher': book['publisher'],
            'year': book['year'],
            'pages': book['pages']
        })


def get_books_from_csv():
    with open('books.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        books = [row for row in reader]
    return books

@app.route('/', methods=['GET'])
def get_books():
    form = BookForm(request.form)
    books = get_books_from_csv()
    print('hello')
    return render_template('books.html', books=books, form=form)
  

@app.route('/', methods=['POST'])
def add_books():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        author = form.author.data
        publisher = form.publisher.data
        year = form.year.data
        pages = form.pages.data
        book = {'title': title, 'author': author, 'publisher': publisher, 'year': year, 'pages': pages}
        save_book_to_csv(book)
        books = get_books_from_csv()
        form.title.data = ''  
        form.author.data = ''
        form.publisher.data = ''
        form.year.data = ''
        form.pages.data = ''
        print("hi")
        return render_template('books.html', books=books, form=form)
    return render_template('books.html', form=form)

@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = get_books_from_csv()
    book_to_delete = None
    for book in books:
        if int(book['id']) == book_id:
            book_to_delete = book
            break
    if book_to_delete:
        books.remove(book_to_delete)
        with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'author', 'publisher', 'year', 'pages']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book)
        flash('Book deleted successfully', 'success')
    else:
        flash('Book not found', 'danger')
    return redirect(url_for('get_books'))

if __name__ == '__main__':
    app.run(debug=True)
