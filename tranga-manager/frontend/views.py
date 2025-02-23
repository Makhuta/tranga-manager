from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from database.models import API
from connector.views import get_connection
from .forms import APIForm
from .functions import custom_render, get_apis

import json

# Create your views here.

@login_required
def index(request):
    return custom_render(request, "index.html")

@login_required
def my_logout(request):
    logout(request)
    return redirect('index')

@login_required
def view_api(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    
    try:
        return custom_render(request, "api.html", {'api': api.first(), 'connectors': get_connection(api.first().ip, api.first().port, api.first().timeout, f'Connectors', ["NONE FOUND"])})
    except:
        return redirect('index')

@login_required
def view_manga(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    internalId = request.GET.get("internalId")
    connector = request.GET.get("connector")
    if not internalId or not connector:
        return redirect('api', pk)
    
    try:
        chapters = get_connection(api.first().ip, api.first().port, path=f'Manga/Chapters?connector={connector}&internalId={internalId}', default=[])
    except:
        return redirect('api', pk)
    if len(chapters) == 0:
        return redirect('api', pk)
    
    return custom_render(request, "manga.html", {'api': api.first(), 'manga': chapters[0].get("parentManga", {'sortName': "UNKNOWN"}), 'chapters': json.dumps(chapters), 'connector': connector})

@login_required
def delete_api(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    if request.method == 'POST':
        api.delete()
        return redirect('index')
    
    return custom_render(request, "api.html", {'api': api.first()})

@login_required
def monitor_api(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    if request.method == 'POST':
        return redirect('api', pk)
    try:
        connectors = get_connection(api.first().ip, api.first().port, api.first().timeout, f'Connectors', ["NONE FOUND"])
        return custom_render(request, "api_monitor.html", {'api': api.first(), 'connectors': connectors})
    except:
        return redirect('api', pk)

@login_required
def add_api(request):
    errors = []
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            api = API(name=data.get('name', ''), ip_or_hostname=data.get('ip'), port=data.get('port'), timeout=data.get('timeout', 1))
            if api.try_save():
                return redirect('index')
            else:
                errors.append("API with IP and Port already exist.")
    else:
        form = APIForm()

    return custom_render(request, 'api_add.html', {'form': form, 'errors': errors})