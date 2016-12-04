from django.contrib import admin

from .models import Book, Rating, Cluster

# adds search filters for admin
class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('book', 'user_name', 'rating')
    list_filter = ['user_name']

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

admin.site.register(Book)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Cluster, ClusterAdmin)
