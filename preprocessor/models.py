# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=500)
    # TODO: Include default center of location bounds or compute dynamically from bounds
    # TODO: Include default predefined means

    def __str__(self):
        return self.name