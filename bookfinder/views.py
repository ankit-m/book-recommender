from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import IdeaForm
from .models import Rating, Book, Cluster
from django.contrib.auth.models import User
from .suggestions import update_clusters
from gensim.summarization import keywords
import datetime
import requests
import json

def add_book(volume, user_name):
    book, created = Book.objects.get_or_create(
        gid = volume['id'],
        title = volume['title'],
        author = volume['author'],
        description = volume['description']
    )
    rating, created = Rating.objects.get_or_create(
        book = book,
        user_name = user_name,
        rating = 1.0
    )
    book.save()
    rating.save()

def make_api_call(payload):
    URL = 'https://www.googleapis.com/books/v1/volumes?q='
    for i in payload:
        URL += i + ','
    URL = URL[:-1]
    print URL
    r = json.loads(requests.get(URL).text)
    return r

@login_required
def home(request):
    form = IdeaForm()
    user_name = request.user.username
    book_list = []
    if request.method == 'POST':
        books = make_api_call(str(keywords(request.POST.get('idea'))).split('\n'))
        for book in books['items']:
            volume = {}
            volume['title'] = book['volumeInfo']['title']
            volume['id'] = book['id']
            try:
                volume['description'] = book['volumeInfo']['description']
            except KeyError:
                volume['description'] = 'Not available'
            try:
                volume['author'] = book['volumeInfo']['authors'][0]
            except KeyError:
                volume['author'] = 'Not Available'
            book_list.append(volume)
            add_book(volume, user_name)
        return render(request, 'bookfinder/home.html', {'form': form, 'book_list': book_list})
    return render(request, 'bookfinder/home.html', {'form': form})

def book_list(request):
    book_list = Book.objects.order_by('-name')
    context = {'book_list':book_list}
    return render(request, 'bookfinder/book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookfinder/book_detail.html', {'book': book})

@login_required
def user_recommendation_list(request):
    # user_reviews = Rating.objects.filter(user_name=request.user.username).prefetch_related('book')
    # user_reviews_book_ids = set(map(lambda x: x.book.id, user_reviews))
    # book_list = Book.objects.exclude(id__in=user_reviews_book_ids)

    user_reviews = Rating.objects.filter(user_name=request.user.username).prefetch_related('book')
    user_reviews_book_ids = set(map(lambda x: x.book.id, user_reviews))
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    other_users_reviews = \
        Rating.objects.filter(user_name__in=other_members_usernames) \
            .exclude(book__id__in=user_reviews_book_ids)
    other_users_reviews_book_ids = set(map(lambda x: x.book.id, other_users_reviews))

    book_list = sorted(
        list(Book.objects.filter(id__in=other_users_reviews_book_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )

    return render(
        request,
        'bookfinder/user_recommendation_list.html',
        {'username': request.user.username, 'book_list': book_list})
