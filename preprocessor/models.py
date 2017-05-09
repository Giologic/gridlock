# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djgeojson.fields import GeometryCollectionField


class Location(models.Model):
    name = models.CharField(max_length=250)
    geojson = GeometryCollectionField()
