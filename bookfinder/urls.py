from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /book/
    url(r'^book$', views.book_list, name='book_list'),
    # ex: /book/5/
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^book/(?P<book_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
]
