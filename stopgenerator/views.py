# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .computations import LatticeLayout, RandomLayout, NBlobLayout


@csrf_exempt
def generate_stop_layout(request):
    if request.method == 'POST':
        stop_layout_nodes = LatticeLayout(20, 350, (120.9747, 14.5896)).generate()
        for n in stop_layout_nodes:
            print(n.coordinates)
        return JsonResponse({'stop_layout_nodes': [n.__dict__ for n in stop_layout_nodes]})
