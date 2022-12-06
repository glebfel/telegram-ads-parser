![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=badge&logo=redis&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)

# TelegramAdsParser
TelegramAdsParser - утилита для сбора рекламных данных с https://promote.telegram.org/stats/ и их представление через интрефейс RESTful API.

# Как запустить?

**1. Создание .env файла**

Перед запуском необходимо создать *.env* файл в основной директории *app*.

Файл должен содержать переменные по аналогии с *.env.example* (если планируется запуск через docker - следует только добавить нужный *API_KEY*, всё остальное оставьте как есть).

**2. Запуск через docker**

Запустите файл docker-compose из корневой директории проекта с помощью команды:
```
docker compose up 
```

**3. Просмотр результатов**

Перейдите на http://{ip}:{port}/v1, где ip - айпишник вашей машины и port - порт.

Если запуск произошел успешно, то будет выведено сообщение: *This is root path of the v1 API. You can get the documentation on /docs path*.


**4. Остановка скрипта**

Для остановки скрипта введите команду:
```
docker compose down
```

Для удаления всех volumes, связанных с компоузом введите:
```
docker compose down -v
```
