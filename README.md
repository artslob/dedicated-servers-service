# Dedicated servers service

[![Build Status](https://travis-ci.com/artslob/selectel-dedicated-servers.svg?branch=master)](https://travis-ci.com/artslob/selectel-dedicated-servers)
[![codecov](https://codecov.io/gh/artslob/selectel-dedicated-servers/branch/master/graph/badge.svg?token=1hb9cxaZYv)](https://codecov.io/gh/artslob/selectel-dedicated-servers)

## Запуск сервиса
1. Установка:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    ```
2. Запуск тестов:
    ```bash
    python3 -m pytest tests/
    ```
3. Запуск сервиса:
    ```bash
    export FLASK_APP=flaskr
    export FLASK_END=development
    flask init-db
    flask run
    ```
4. Доступные эндпоинты:
    ```
    /rack/all                -- GET
    /rack/<int:id>           -- GET
    /server/all              -- GET
    /server/<int:id>         -- GET
    /server/create           -- POST, input: json, Header: 'Content-Type: application/json'
    /server/update/<int:id>  -- POST, input: json, Header: 'Content-Type: application/json'
    ```

## Статус завершённости
- [ ] Сервис должен писать логи при манипуляциях над сущностями в консоль.
- [x] Сервис должен отвечать на все эндпоинты в формате JSON.
- [x] content-type для всех эндпоинтов должен быть только application/json.
- [x] Сервис должен принимать запросы только в формате JSON.
- [x] Допускается использование GET параметров.
---
- [x] Все сущности должны быть доступны как по  идентификатору, так и списком по группам (все стойки, все серверы).
- [x] Сортировка по умолчанию по идентификатору.
- [x] Нужна возможность указать сортировку по дате.
- [x] Стойки ограничены по размеру серверов:  стойка с 10 и 20 серверами.
- [x] Добавление сервера в стойку невозможно если она заполнена.
- [x] Сервера могут находится в состояниях (Unpaid, Paid, Active, Deleted).
- [x] Переход из Deleted состояний невозможен.
- [x] Переход в Deleted возможен в любой момент.
- [x] Остальные состояния изменяются строго  в порядке следования. Изменения состояния осуществляются запросами в api. 
- [ ] Состояние Paid задается вместе с временной меткой (формат timestamp), которая хранит время перехода в состояние Unpaid.
- [ ] Переход в состояние Active должен происходить автоматически, через случайное количество секунд после переход в состояние Paid, например 5-15 секунд (эмуляция подготовки сервера). 
- [ ] Расчет перехода в состояние Active происходит в момент запроса к сервису.

## Затраченное время
* 7.06: с 11.00 до 19.33
* 9.06: с 20.20 до 22.28
