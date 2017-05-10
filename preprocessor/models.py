# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.name