# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def generate_stop_layout(request):
    if request.method == 'POST':
        return JsonResponse({'stop_layout_nodes': "Hello World!"})
