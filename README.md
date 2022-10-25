![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)

# TelegramAdsParser

TelegramAdsParser - утилита для сбора рекламных данных с https://promote.telegram.org/stats/.

# Как запустить?

**1. Создание .env файла**

Перед запуском необходимо создать *.env* файл в основной директории *app*.

Файл должен содержать переменные по аналогии с *.env.example* (если планируется запуск через docker - следует только добавить нужный *API_KEY*, всё остальное оставьте как есть).

**2. Запуск через docker**

Запустите файл docker-compose из корневой директории срипта с помощью команды:
```
docker compose up 
```

**3. Остановка скрипта**

Для остановки скрипта введите команду:
```
docker compose down
```

Для удаления всех volumes, связанных с компоузом введите:
```
docker compose down -v
```
