# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=500)

    # List of recommended predefined means will be treated as a JSON string
    recommended_predefined_means = models.TextField()

    def __str__(self):
        return self.name
