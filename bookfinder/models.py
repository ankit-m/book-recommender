from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import numpy as np

class Book(models.Model):
    name = models.CharField(max_length = 200)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)

    def __unicode__(self):
        return self.name

class Review(models.Model):
    book = models.ForeignKey(Book)
    user_name = models.CharField(max_length=100)
    rating = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(10.0)])

class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
