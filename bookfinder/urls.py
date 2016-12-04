from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.home, name='home'),
    url(r'^book$', views.book_list, name='book_list'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
