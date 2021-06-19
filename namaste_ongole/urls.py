"""namaste_ongole URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django_ip_geolocation.decorators import with_ip_geolocation
from django.http.response import JsonResponse
from branch.models import Branch
from branch.views import BranchSerializer
from order.models import INTERNET_HANDLING_CHARGES, GST_CHARGES


admin.site.site_header = "Namaste Ongole Admin"
admin.site.site_title = "Nmaste Ongole Admin Portal"
admin.site.index_title = "Welcome to Namaste Ongole Amdin"

schema_view = get_swagger_view(title='Namaste Ongole API')


class SearchRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        request = self.request
        is_mobile = request.user_agent.is_mobile
        is_tablet = request.user_agent.is_tablet
        browser_family = request.user_agent.browser.family
        device_family = request.user_agent.device.family
        os_family = request.user_agent.os.family

        data = 'is_mobile=' + str(is_mobile) + ' | is_tablet=' + str(
            is_tablet
        ) + ' | browser_family=' + browser_family + ' | device_family=' + device_family + ' | os_family=' + os_family
        # url = 'https://google.com/?q=' + data
        ios_app_store_url = "https://www.apple.com/in/ios/app-store/"
        android_app_store_url = "https://play.google.com/store/apps/details?id=com.trangla.tea_bar"

        os = os_family.lower()
        if os == "ios":
            return ios_app_store_url
        elif os == "android":
            return android_app_store_url
        else:
            return android_app_store_url


@with_ip_geolocation
def app_api_settings(request):
    location = request.geolocation
    branch = Branch.objects.get(pk=1)
    details = {}
    if branch:
        details = branch.json
        details["order_info"] = {
            "gst": GST_CHARGES,
            "internet_handling": INTERNET_HANDLING_CHARGES,
            "delivery_charges": branch.delivery_charges,
        }
    details["service_available"] = True
    details["app_info"] = {"android_version": "1.0.0", "ios_version": "1.0.0"}
    details["location"] = location

    details["delivery_slots"] = {
        "slots": [
            {
                "shift": "Morning",
                "delivery_time": "06AM to 08AM",
                "start_time": 12,
                "end_time": 0,
                "info": "Every order after 12PM will be delivered next morning shift"
            },
            {
                "shift": "Evening",
                "delivery_time": "05PM to 07PM",
                "start_time": 0,
                "end_time": 12,
                "info": "Every order before 12PM will be delivered same day evening shift"
            }
        ]
    }

    return JsonResponse(details)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),
    path('user/', include('user.urls')),
    path('', include('order.urls')),
    #path(r'swagger-docs/', schema_view),
    path(r'docs/', include_docs_urls(title='Namaste Ongole API')),
    path('download-app/', SearchRedirectView.as_view()),
    path('info/', app_api_settings),
    # path('download-app/', download_app, name="download_app"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
