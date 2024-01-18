import sys
import os
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.apps import AppConfig
from requests import get

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-0wo^wrqiz46dg1c+ua_+dvhl%q42pftg^+idp2g8y%n7-&-ihh"
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = []
ROOT_URLCONF = "apps"
TEMPLATES = []
TEMPLATE_DIRS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
MIDDLEWARE = []



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
    path("", index),
    path("details", index),
    path("script.js", script),
    path("weather", get_wether)
]


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
