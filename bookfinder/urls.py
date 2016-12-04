from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.home, name='home'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
