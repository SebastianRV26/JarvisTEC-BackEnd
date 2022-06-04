import pickle

import pandas as pd
from django.http import JsonResponse
from django.views import View
from rpy2.robjects import r
from sklearn.preprocessing import StandardScaler

from providers.YoloProvider import YoloProvider
from PIL import Image


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


# GET /RLMinR/<int:model_id>/<str:values>/
class LoadRLMModel(View):
    @staticmethod
    def get(request, model_id, values):
        if model_id == 1:
            model = "BikesModelRLM"
        elif model_id == 2:
            model = "CarsModelRLM"
        elif model_id == 3:
            model = "ClimaModelRLM"
        elif model_id == 4:
            model = "SegurosModelRLM"
        else:
            value = "Modelo invalido"
            response = {'code': 404, 'data': value}
            return JsonResponse(response)

        path = f"./models/{model}.rds"

        try:
            value = load_r_model(path, values)
            response = {'code': 200, 'data': value}
            return JsonResponse(response)
        except ValueError:
            value = "Hay mas o menos parametros de los esperados, intente de nuevo"
            response = {'code': 400, 'data': value}
            return JsonResponse(response)


def load_python_model(file_path, columns_names, rows, scale=False):
    model_reloaded = pickle.load(open(file_path, 'rb'))

    # convert list into DataFrame
    df = pd.DataFrame(rows).transpose()
    df.columns = columns_names

    if scale:
        scaler = StandardScaler()
        df = scaler.fit_transform(df)

    result = model_reloaded.predict(df)[0]
    print(f"result of {file_path} = {result}")
    return result


# GET /pythonModel/<int:model_id>/
class LoadDecisionTreePython(View):
    @staticmethod
    def get(request, model_id, rows_values):
        if model_id == 1:
            name = "telco_model"
            columns = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TechSupport']
        elif model_id == 2:
            name = "avocado_model"
            columns = ['Total Volume', '4046', '4225', '4770', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags',
                       'type', 'year']
        elif model_id == 3:
            name = "wine_model"
            columns = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
                       'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'white']
        elif model_id == 4:
            name = "companyInventory"
            columns = ['store', 'item', 'year', 'month', 'day', 'week', 'weekofyear',
                       'dayofweek', 'weekday', 'dayofyear', 'quarter']
        elif model_id == 5:
            name = "S&P500stock"
            columns = ['Numbers']
        elif model_id == 6:
            name = "bodyfat-model"
            columns = ['Density', 'Chest', 'Abdomen']
        elif model_id == 7:
            name = "hepatitis-model"
            columns = ['Sex', 'Age', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE', 'CHOL', 'CREA', 'GGT', 'PROT']
        elif model_id == 8:
            name = "stroke-model"
            columns = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
                       'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']
        else:
            value = "Modelo invalido"
            response = {'code': 404, 'data': value}
            return JsonResponse(response)
        path = f"./models/{name}.sav"

        rows = rows_values.split(',')
        try:
            if model_id == 6 or model_id == 7 or model_id == 8:
                value = load_python_model(path, columns, rows, True)
            else:
                value = load_python_model(path, columns, rows)
            response = {'code': 200, 'data': str(value)}
            return JsonResponse(response)
        except ValueError:
            value = "Hay mas o menos parametros de los esperados, intente de nuevo con la cantidad correcta de parametros"
            response = {'code': 400, 'data': value}
            return JsonResponse(response)


class ObjectDetector(View):
    def get(self, request):
        video_url = self.request.GET.get('url')
        if YoloProvider.thread_is_running():
            return {'code': 200, 'data': "Ya hay un proceso corriendo"}
        YoloProvider.run_thread(video_url)
        return JsonResponse({'code': 200, 'data': {}})


class DetectorResults(View):
    @staticmethod
    def get(request):
        if YoloProvider.thread_is_running():
            return JsonResponse({'code': 200, 'data': "Proceso corriendo"})
        return JsonResponse({'code': 200, 'data': YoloProvider.get_detections()})


class FaceApi(View):
    @staticmethod
    def post(request):
        file = request.FILES["data"]
        img = Image.open(file)
        img.show()
        return JsonResponse({'code': 200, 'data': "Face"})
