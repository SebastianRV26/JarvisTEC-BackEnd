# load RModel (RLM)
from rpy2.robjects import r


def load_r_model(file_path, values):
    result = r(f'''
        model <- readRDS('{file_path}', refhook = NULL)
        ModelRLM <- data.frame({values})
        ModelRLM.prediction <-predict(model, newdata = ModelRLM)
        ModelRLM.prediction
    ''')[0]
    print(f"result of {file_path} = {result}")
    return result


file = 'BikesModelRLM.rds'
values = "distance=0.7, driver.AF8.tip=1.83"
load_r_model(file, values)

import pickle
import pandas as pd


# load PythonModel (desition tree)
def load_python_model(file_path, columns_names, rows):
    model_reloaded = pickle.load(open(file_path, 'rb'))

    # convert list into DataFrame
    df = pd.DataFrame(rows).transpose()
    df.columns = columns_names

    result = model_reloaded.predict(df)[0]
    print(f"result of {file_path} = {result}")
    return result


file = 'telco_model.sav'
columns = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TechSupport']
rows = [[1], [68.65], [68.65], [0]]
load_python_model(file, columns, rows)
