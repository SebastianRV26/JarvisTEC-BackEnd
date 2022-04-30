# JarvisTEC-BackEnd

JarvisTEC - FrontEnd [aquí](https://github.com/SebastianRV26/JarvisTEC-FrontEnd)

## Endpoints

Se crearon dos endpoints:
* El primero para los modelos creados en R:
```
GET /RLMinR/<int:model_id>/<str:values>/
```
Donde model_id es el identificador del modelo `(1 - 4)` y values son las columnas y el valor requerido del modelo, por ejemplo `bmi=70,age=18`

* El segundo para los modelos creados en python:
```
GET /pythonModel/<int:model_id>/<str:rows_values>/
```
Donde model_id es el identificador del modelo `(1 - 8)` y rows_values solo los valores de las columnas requeridas, siguiendo el ejemplo anterior sería: `70,18`

## Cómo se exportaron los modelos

En python
```python
import pickle

# save the model to disk
filename = 'model_name.sav'
pickle.dump(model, open(filename, 'wb'))
```

En R
```r
install.packages("e1071")
library(e1071)

MODEL_SAVE_PATH = "ModelName"
model_path = './res'
DEP_LIBS = c("e1071")

# save
model_rds_path = paste(MODEL_SAVE_PATH, ".rds",sep='')

# save model
dir.create(dirname(model_path), showWarnings=FALSE, recursive=TRUE)
saveRDS(model, model_rds_path)

# save dependency list
file_conn <- file(model_dep_path)
writeLines(DEP_LIBS, file_conn)
close(file_conn)
```

## Cómo ejecutarlo

Es necesario ejecutar los siguientes comandos:

```
pip install numpy pandas rpy2 sklearn 
pip install Django==4.0.4
pip install django-cors-headers
```

En la carpeta del proyecto:
```
python manage.py runserver
```

## Integrantes:
* [Ali Hashemi Shirkavand](https://github.com/AliHashemiS)
* [Francisco Soto Quesada](https://github.com/franrsq)
* [Jairo Pacheco Campos](https://github.com/JairoPacheco)
* [Sebastián Rojas Vargas](https://github.com/SebastianRV26)

Curso: Inteligencia Artificial.
I Semestre 2022.
Profesor: Efrén Jimenez.