from django.contrib import admin

from .models import Book, Review, Cluster

# adds search filters for admin
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('book', 'user_name', 'rating')
    list_filter = ['user_name']
    search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

admin.site.register(Book)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
