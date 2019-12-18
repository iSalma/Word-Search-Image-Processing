
from django.contrib import admin
from django.urls import path
from output.views import ProcessAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('output/', ProcessAPI.as_view())
]
