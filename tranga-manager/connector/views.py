from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from database.models import API

import requests

def test_connection(ip, port, timeout=10):
    url = f'http://{ip}:{port}/Ping'
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.json() == 'Pong' if resp.ok else False
    except:
        return False
    
def req_connection(ip, port, timeout=None, path="Ping", default={}):
    url = f'http://{ip}:{port}/{path}'
    try:
        if timeout is not None:
            resp = requests.get(url, timeout=timeout)
        else:
            resp = requests.get(url)
        return resp.json() if resp.ok else default
    except:
        return default
    
def post_connection(ip, port, timeout=None, path=""):
    url = f'http://{ip}:{port}/{path}'
    try:
        if timeout is not None:
            return requests.post(url, timeout=timeout).ok
        return requests.post(url).ok
    except:
        return False
    
def req_image(ip, port, timeout=10, path=""):
    url = f'http://{ip}:{port}/{path}'
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp
    except:
        return None

# Create your views here.
@login_required
def ping(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'online': False})
    return JsonResponse(data={'online': test_connection(api.first().ip, api.first().port, api.first().timeout) })
    

@login_required
def test(request):
    ip = request.GET.get("ip")
    port = request.GET.get("port")
    if not ip or not port:
        return JsonResponse(data={'success': False })
    return JsonResponse(data={'success': test_connection(ip, port) })

@login_required
def jobs_monitor(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': req_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/MonitorJobs", []) })

@login_required
def jobs_waiting(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': req_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/Waiting", []) })

@login_required
def jobs_running(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': req_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/Running", []) })


@login_required
def manga_cover(request):
    pk = request.GET.get("pk")
    internalId = request.GET.get("internalId")
    if not pk or not internalId:
        return HttpResponse("Failed to fetch image", status=500)

    api = API.objects.filter(pk=pk)
    if not api.exists():
        return HttpResponse("Failed to fetch image", status=500)
    
    cover = req_image(api.first().ip, api.first().port, api.first().timeout, f'Manga/Cover?internalId={internalId}')
    if cover is None:
        return HttpResponse("Failed to fetch image", status=500)
    
    return HttpResponse(cover.content, content_type=cover.headers.get("Content-Type", "image/jpeg"))


@login_required
def manga_search(request):
    pk = request.GET.get("pk")
    connector = request.GET.get("connector")
    title = request.GET.get("title")
    if not pk or not connector or not title:
        return HttpResponse("Failed to fetch image", status=500)
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': req_connection(api.first().ip, api.first().port, path=f'/Manga/FromConnector?connector={connector}&title={title}', default=[]) })

@login_required
def manga_monitor(request):
    pk = request.POST.get("pk")
    connector = request.POST.get("connector")
    internalId = request.POST.get("internalId")
    interval = request.POST.get("interval")
    translatedLanguage = request.POST.get("translatedLanguage")
    print(pk, connector, internalId, interval, translatedLanguage)
    if not pk:
        return JsonResponse(data={'success': False})
    if not connector or not internalId or not interval or not translatedLanguage:
        return JsonResponse(data={'success': False})
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': False})
    return JsonResponse(data={'success': post_connection(api.first().ip, api.first().port, api.first().timeout, f'Jobs/MonitorManga?connector={connector}&internalId={internalId}&interval={interval}&translatedLanguage={translatedLanguage}')})


@login_required
def connectors(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': req_connection(api.first().ip, api.first().port, api.first().timeout, f'Connectors', []) })