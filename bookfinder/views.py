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
        description = volume['description'],
        url = volume['url']
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
        inp = request.POST.get('idea')
        try:
            words = keywords(inp)
        except Exception:
            return render(request, 'bookfinder/home.html', {'form': form, 'error': 'Please type more.'})
        if len(words) != 0:
            books = make_api_call(str(words).split('\n'))
            for book in books['items']:
                volume = {}
                volume['title'] = book['volumeInfo']['title']
                volume['id'] = book['id']
                volume['url'] = book['selfLink']
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
                update_clusters()
            return render(request, 'bookfinder/home.html', {'form': form, 'book_list': book_list})
        else:
            return render(request, 'bookfinder/home.html', {'form': form, 'error': 'Please type more.'})
    return render(request, 'bookfinder/home.html', {'form': form})

@login_required
def user_recommendation_list(request):
    user_ratings = Rating.objects.filter(user_name=request.user.username).prefetch_related('book')
    user_ratings_book_ids = set(map(lambda x: x.book.id, user_ratings))
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    other_users_ratings = \
        Rating.objects.filter(user_name__in=other_members_usernames) \
            .exclude(book__id__in=user_ratings_book_ids)
    other_users_ratings_book_ids = set(map(lambda x: x.book.id, other_users_ratings))

    book_list = list(Book.objects.filter(id__in=other_users_ratings_book_ids))

    return render(
        request,
        'bookfinder/user_recommendation_list.html',
        {'username': request.user.username, 'book_list': book_list})
