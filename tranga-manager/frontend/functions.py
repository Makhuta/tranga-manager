from django.shortcuts import render, redirect
from datetime import date

from database.models import API

def get_apis():
    apis = API.objects.all()
    if len(apis) == 0:
        return []
    return apis

def custom_render(request, template_name, context={}):
    default_context = {
        'year': date.today().strftime("%Y"),
        'base_url': f'{request.scheme}://{request.get_host()}',
        'apis': get_apis(),
    }

    context.update(default_context)
    return render(request, template_name, context)