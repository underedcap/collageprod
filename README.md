*Сырой, но уже рабочий бот для продажи VPN сабок / конфигов.
Пока что MVP-заготовка, но основная логика уже есть.*

## Логика

```text id="x0x0ci"
tg bot -> back -> db
```


<img width="1115" height="970" alt="image" src="https://github.com/user-attachments/assets/e2ee9411-4f90-482b-89ea-fee835410bb6" />


## Сейчас есть

* таблица под логи покупки сабок
* авто-клир истекших сабок
* +- какой то UI
* контейнеризация
* базовый backend
* MySQL

## Ports

```yaml id="0t8w4h"
MySQL:
  ports:
    - "3307:3306"

back:
  8080
```

## Запуск

docker compose up --build
```

## ENV

```env id="f5x0ya"
BOT_TOKEN=your_token

DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=insightdlc
```

## TODO

* подключить платежку
* авто-выдачу конфигов
* админку
* webhook mode
* нормальный rate limit
* статистику

## Status

На данный момент это просто рабочий сырой бот в контейнере для продажи сабок.
Если хотите — форкайте и допиливайте под себя.
