from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date

from database.models import API
from connector.views import req_connection
from .forms import APIForm

# Create your views here.

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
    
    return custom_render(request, "api.html", {'api': api.first()})

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
        #api.delete()
        return redirect('api', pk)
    return custom_render(request, "api_monitor.html", {'api': api.first(), 'connectors': req_connection(api.first().ip, api.first().port, api.first().timeout, f'Connectors', ["NONE FOUND"])})

@login_required
def add_api(request):
    errors = []
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            api = API(name=data.get('name', ''), ip=data.get('ip'), port=data.get('port'), timeout=data.get('timeout', 1))
            if api.try_save():
                return redirect('index')
            else:
                errors.append("API with IP and Port already exist.")
    else:
        form = APIForm()

    return custom_render(request, 'api_add.html', {'form': form, 'errors': errors})