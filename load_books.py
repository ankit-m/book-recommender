import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blockbuster.settings")

import django
django.setup()

from bookfinder.models import Book


def save_book_from_row(book_row):
    book = Book()
    book.id = book_row[0]
    book.name = book_row[1]
    book.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        books_df = pd.read_csv(sys.argv[1])
        print books_df

        books_df.apply(
            save_book_from_row,
            axis=1
        )

        print "There are {} books".format(Book.objects.count())

    else:
        print "Please, provide Book file path"
