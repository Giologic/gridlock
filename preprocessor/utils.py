# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from gridlock.settings import DATA_FILES_ROOT


def get_location_geometry(location):
    location_file = open(os.path.join(DATA_FILES_ROOT, location.path))
    return json.load(location_file)
