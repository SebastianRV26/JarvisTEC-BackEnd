from django.urls import path

from .views import Endpoints, GetByValue, LoadRLMModel, LoadDecisionTreePython, ObjectDetector, DetectorResults, \
    FaceApi, VoiceApi

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get/', Endpoints.as_view(), name='endpoint'),
    path('get/<str:value>/', GetByValue.as_view(), name='getByValue'),
    path('RLMinR/<int:model_id>/<str:values>/', LoadRLMModel.as_view(), name='RModel'),
    path('pythonModel/<int:model_id>/<str:rows_values>/', LoadDecisionTreePython.as_view(), name='PythonModel'),
    path('objectDetector/', ObjectDetector.as_view(), name='objectDetector'),
    path('detectorResults/', DetectorResults.as_view(), name='detectorResults'),
    path('face/', FaceApi.as_view(), name='face'),
    path('voice/', VoiceApi.as_view(), name='voice'),
]
