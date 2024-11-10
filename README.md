<h1 align="center">Проект конвертации валют: CurrencyConverterAPI</h1>

## Данный проект представляет собой API с использованием Django Rest Framework, базой Postgres и сервиса ExchangeRate-API с последующей сборкой в Docker.

### Проект выполнен группой ЭМС-171, команда ITSuperFriends: Овчинников, Ликсюткина, Лисица, Юсипов.

### 1. Установка зависимостей.
``` 
pip install -r requirements.txt
```

### 2. Создать свой .env файл в корне проекта.

### 3. Заполнить .env файл:
```xml
DB_NAME=db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=locahost
SECRET_KEY=django-insecure-ptxj-r*tqh1#08n+2+09582l%q(2nctus0z_4=0)93ly0n%2$8
DEBUG=True
EXCHANGE_RATE_API_KEY=347aedda8f157b2e2cf1b4ab
```


### 4. Выполнить миграции.
```sh
python ./manage.py migrate 
```

### 5. Запустить сервер.
```sh
python ./manage.py runserver
```
### 6. Запуск всех образов.
```sh
docker-compose up --build -d
```
