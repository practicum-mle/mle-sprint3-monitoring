from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
import numpy as np
from prometheus_client import Histogram
# ваш код здесь — необходимый импорт
from prometheus_client import Counter
# создание экземпляра FastAPI-приложения
app = FastAPI()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

main_app_predictions = Histogram(
    # имя метрики
    "main_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets=(1, 2, 4, 5, 10)
)


# ваш код здесь — объект для сбора метрики
main_positive_counter = Counter('main_positive_counter', 'Count positive result')


@app.get("/predict")
def predict(x: int, y: int):
    np.random.seed(x)
    prediction = x+y + np.random.normal(0,1)
    main_app_predictions.observe(prediction)
    if prediction > 0:
        main_positive_counter.inc()
    
    # ваш код здесь — увеличение метрики счётчика
    
    return {'prediction': prediction}
