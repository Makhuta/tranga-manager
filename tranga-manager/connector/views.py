from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from urllib.parse import urlencode

from database.models import API
from frontend.functions import custom_render


from langcodes import *
import requests

def test_connection(ip, port, timeout=10):
    url = f'http://{ip}:{port}/Ping'
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.json() == 'Pong' if resp.ok else False
    except:
        return False
    
def req_connection(url, timeout=None, method="GET"):
    if timeout is not None:
        return requests.request(method=method, url=url, timeout=timeout)
    return requests.request(method=method, url=url)
    
def get_connection(ip, port, timeout=None, path="Ping", default={}):
    url = f'http://{ip}:{port}/{path}'
    try:
        if timeout is not None:
            resp = req_connection(url, timeout=timeout)
        else:
            resp = req_connection(url)
        return resp.json() if resp.ok else default
    except:
        return default
    
def post_connection(ip, port, timeout=None, path=""):
    url = f'http://{ip}:{port}/{path}'
    try:
        if timeout is not None:
            return req_connection(url=url, method="POST", timeout=timeout).ok
        return req_connection(url=url, method="POST").ok
    except:
        return False
    
def delete_connection(ip, port, timeout=None, path=""):
    url = f'http://{ip}:{port}/{path}'
    try:
        if timeout is not None:
            return req_connection(url=url, method="DELETE", timeout=timeout).ok
        return req_connection(url=url, method="DELETE").ok
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
    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/MonitorJobs", []) })

@login_required
def jobs_waiting(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/Waiting", []) })

@login_required
def jobs_running(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, api.first().timeout, "Jobs/Running", []) })


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
    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, path=f'/Manga/FromConnector?connector={connector}&title={title}', default=[]) })

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
def start_manga(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    connector = request.POST.get("connector")
    internalId = request.POST.get("internalId")
    source_url = request.POST.get("source_url")
    if not connector or not internalId or not source_url:
        return redirect('api', pk)
    
    post_connection(api.first().ip, api.first().port, api.first().timeout, f'Jobs/StartNow?jobId=Tranga.Jobs.DownloadNewChapters-{internalId}')
    params = {
        'internalId': internalId,
        'connector': connector
    }
    return redirect(f'{request.build_absolute_uri(source_url)}?{urlencode(params)}')


@login_required
def cancel_manga(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    connector = request.POST.get("connector")
    internalId = request.POST.get("internalId")
    source_url = request.POST.get("source_url")
    if not connector or not internalId or not source_url:
        return redirect('api', pk)
    
    post_connection(api.first().ip, api.first().port, api.first().timeout, f'Jobs/Cancel?jobId=Tranga.Jobs.DownloadNewChapters-{internalId}')
    params = {
        'internalId': internalId,
        'connector': connector
    }
    return redirect(f'{request.build_absolute_uri(source_url)}?{urlencode(params)}')


@login_required
def delete_manga(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return redirect('index')
    connector = request.POST.get("connector")
    internalId = request.POST.get("internalId")
    source_url = request.POST.get("source_url")
    if not connector or not internalId or not source_url:
        return redirect('api', pk)
    
    url = f'http://{api.first().ip}:{api.first().port}/Jobs?jobId=Tranga.Jobs.DownloadNewChapters-{internalId}'
    if not req_connection(method='OPTIONS', url=url).ok:
        params = {
            'internalId': internalId,
            'connector': connector
        }
        return redirect(f'{request.build_absolute_uri(source_url)}?{urlencode(params)}')
    
    delete_connection( api.first().ip, api.first().port, path=f'Jobs?jobId=Tranga.Jobs.DownloadNewChapters-{internalId}')
    return redirect('api', pk)


@login_required
def connectors(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, api.first().timeout, f'Connectors', []) })

@login_required
def connectors_languages(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': {}})
    connector = request.GET.get("connector")
    if not connector:
        return JsonResponse(data={'success': {}})

    return JsonResponse(data={'success': get_connection(api.first().ip, api.first().port, api.first().timeout, f'Languages?connector={connector}', {"name": connector, "SupportedLanguages": ['en', 'it', 'de']}) })

@login_required
def language_name(request):
    language = request.GET.get("language")
    if not language:
        return JsonResponse(data={'success': "unknown"})

    lang = Language.get(language)
    return JsonResponse(data={'success': lang.display_name() })


@login_required
def chapters(request, pk):
    api = API.objects.filter(pk=pk)
    if not api.exists():
        return JsonResponse(data={'success': []})
    connector = request.GET.get("connector")
    internalId = request.GET.get("internalId")
    if not connector or not internalId:
        return JsonResponse(data={'success': []})
    resp = get_connection(api.first().ip, api.first().port, path=f'Manga/Chapters?internalId={internalId}&connector={connector}', default=[])
    items = []
    ret = []
    for item in resp:
        key = ( item.get("volumeNumber", 0), item.get("chapterNumber", 0) )
        if key in items:
            continue
        items.append(key)
        ret.append(item)
    return JsonResponse(data={'success': ret })