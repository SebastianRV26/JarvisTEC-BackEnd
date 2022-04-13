from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rpy2.robjects import r
import pickle
import pandas as pd


class Endpoints(View):
    def get(self, request):
        response = [{'code': 200, 'data': {}}]
        return JsonResponse(response, safe=False)  # Falso: array de JSON, True devolver un JSON


class GetByValue(View):
    @staticmethod
    def get(request, value):
        response = {'code': 200, 'data': value}
        return JsonResponse(response)


def load_r_model(file_path, values):
    result = r(f'''
        model <- readRDS('{file_path}', refhook = NULL)
        ModelRLM <- data.frame({values})
        ModelRLM.prediction <-predict(model, newdata = ModelRLM)
        ModelRLM.prediction
    ''')[0]
    print(f"result of {file_path} = {result}")
    return result


# GET /RLMinR/<str:values>/
class LoadRLMModel(View):
    @staticmethod
    def get(request, values):
        path = "./models/BikesModelRLM.rds"

        value = load_r_model(path, values)
        response = {'code': 200, 'data': value}
        return JsonResponse(response)


def load_python_model(file_path, columns_names, rows):
    model_reloaded = pickle.load(open(file_path, 'rb'))

    # convert list into DataFrame
    df = pd.DataFrame(rows).transpose()
    df.columns = columns_names

    result = model_reloaded.predict(df)[0]
    print(f"result of {file_path} = {result}")
    return result


# GET /pythonModel/
class LoadDecisionTreePython(View):
    @staticmethod
    def get(request):
        path = "./models/telco_model.sav"
        columns = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TechSupport']
        rows = [[1], [68.65], [68.65], [0]]
        value = load_python_model(path, columns, rows)
        response = {'code': 200, 'data': str(value)}
        return JsonResponse(response)