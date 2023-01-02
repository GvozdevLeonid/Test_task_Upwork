from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import asyncio
import aiohttp
from .models import *


def index(request):
    if request.user.is_authenticated:
        urls = [{"url": url.url, "id": url.id} for url in URL.objects.all()]

        context = {"items": asyncio.run(check_urls(urls))}
        return render(request, template_name="index.html", context=context)
    else:
        return HttpResponse("<H1 style='text-align:center; margin-top: 40vh;'>I'm Sorry permission denied!<br> Please <a href='/accounts/login/'>login</a></H1>")

def update(request):
    data = request.POST
    urls = [{"url": data[key].strip(), "id":key} for key in data.keys()]

    return JsonResponse(asyncio.run(check_urls(urls)), safe=False)


async def test_url(session, url):
    try:
        async with session.get(url=url["url"], ssl=False) as resp:
            if resp.status == 200:
                return {"url": url["url"], "status": "ok", "id": url["id"]}
    except aiohttp.ClientConnectorError:
        pass
    except aiohttp.InvalidURL:
        return {"url": url["url"], "status": "invalid", "id": url["id"]}

    return {"url": url["url"], "status": "bad", "id": url["id"]}


async def check_urls(urls):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(test_url(session, url))
            tasks.append(task)

        result = asyncio.gather(*tasks)
        await result

    return result.result()

