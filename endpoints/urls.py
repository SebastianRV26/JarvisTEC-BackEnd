from django.urls import path, include
from .views import Endpoints, GetByValue

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get/', Endpoints.as_view(), name='endpoint'),
    path('get/<str:value>/', GetByValue.as_view(), name='getByValue'),
]
