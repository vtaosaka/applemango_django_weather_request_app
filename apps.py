from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.apps import AppConfig
from requests import get


def render(path: str, content_type: str = "text/html; charset=utf-8"):
    with open(path) as f:
        return HttpResponse(f.read(), content_type=content_type)

class RequestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "request"

def index(request):
    return render("index.html")


def script(request):
    return render("script.js", "text/javascript; charset=utf-8")


def get_weather(params: int):
    url = f"https://weather.tsukumijima.net/api/forecast?city={params}"
    return get(url, verify=False).json()


def q(r, n, d=None):
    return r.GET.get(n) or d

def qi(r, n, d=None):
    return int(q(r, n, d))

def get_wether(request):
    params = qi(request, "id")
    data = get_weather(params)["forecasts"][0]
    context = {
        "weather": {
            "date": data["date"],
            "telop": data["telop"],
            "temperature": {
                "max": data["temperature"]["max"]["celsius"],
                "min": data["temperature"]["min"]["celsius"],
            },
        },
        "weathers": data,
        "city": q(request, "city"),
        "image": {
            "tag": data["image"]["title"],
            "url": data["image"]["url"],
        },
    }
    return JsonResponse(context)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("details", index),
    path("script.js", script),
    path("weather", get_wether)
]