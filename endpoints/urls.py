from django.urls import path, include
from .views import Endpoints, GetByValue, LoadRLMModel, LoadDecisionTreePython

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get/', Endpoints.as_view(), name='endpoint'),
    path('get/<str:value>/', GetByValue.as_view(), name='getByValue'),
    path('RLMinR/<str:values>/', LoadRLMModel.as_view(), name='RModel'),
    path('pythonModel/', LoadDecisionTreePython.as_view(), name='RModel'),
]
