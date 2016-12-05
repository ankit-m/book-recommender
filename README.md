Blockbuster
===========
A Collaborative Book Recommender System
----------------------------------------

### Installation

To run the development version of the code you need to have `python 2.7^` along with `pip` package manager. To install all the dependencies, run

```bash
pip install -r requirements.txt
```

### File structure

.
|-- blockbuster
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- bookfinder
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- migrations
|   |-- models.py
|   |-- suggestions.py
|   |-- templates
|   |   `-- bookfinder
|   |       |-- home.html
|   |       `-- user_recommendation_list.html
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- db.sqlite3
|-- manage.py
|-- Procfile
|-- README.md
|-- requirements.txt
`-- templates
    |-- base.html
    `-- registration

### Pipeline

This project uses Google Books API, Gensim API and Scikit Learn. The data flow in the project is as follows:-
1. User submits idea in the root view
2. Gensim finds the keywords and Google Books API retreives similar books to the idea and displays on page
3. The 'Book Suggestions' tab contains the recommended list of books for the user.

For a more detailed explanation refer to the report.
