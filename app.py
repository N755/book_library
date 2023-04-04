from flask import Flask, render_template, request
from wtforms import Form, StringField, IntegerField, validators
import csv

app = Flask(__name__)
app.config['DEBUG'] = True


class BookForm(Form):
    title = StringField('Назва', [validators.Length(min=1, max=50)])
    author = StringField('Автор', [validators.Length(min=1, max=50)])
    publisher = StringField('Видавництво', [validators.Length(min=1, max=50)])
    year = IntegerField('Рік випуску', [validators.NumberRange(min=1000, max=9999)])
    pages = IntegerField('Кількість сторінок', [validators.NumberRange(min=1)])

def save_book_to_csv(book):
    with open('books.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author', 'publisher', 'year', 'pages']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
    'title': book['title'],
    'author': book['author'],
    'publisher': book['publisher'],
    'year': book['year'],
    'pages': book['pages']
})


# def get_books_from_csv():
#     with open('books.csv', newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         books = [row for row in reader]
#     return books

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookForm(request.form)
    # if request.method == 'GET':
    #     books = get_books_from_csv()
        # return render_template('books.html', books=books)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        author = form.author.data
        publisher = form.publisher.data
        year = form.year.data
        pages = form.pages.data
        book = {'title': title, 'author': author, 'publisher': publisher, 'year': year, 'pages': pages}
        save_book_to_csv(book)
        return 'Дані про книгу збережено: {} - {} - {} - {} - {}\n'.format(title, author, publisher, year, pages) 
    return render_template('books.html', form=form)
# @app.route('/books')
# def books():
#     books = get_books_from_csv()
#     return render_template('books.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)