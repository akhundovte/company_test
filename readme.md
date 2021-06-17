### company_test
 

**Запуск проекта**  

- Переход в папку с файлом docker-compose.yml  
```console
cd deploy/company_test
``` 

- Создание образов  
```console
docker-compose build
```

- Запуск контейнеров  
```console
docker-compose up -d
```

- Применение миграций  
```console
docker-compose exec company_test python manage.py migrate
```

- Создание пользователя с правами администратора  
```console
docker-compose exec company_test python manage.py createadmin
```

**Адрес в браузере**  
http://localhost:8080  

**Авторизация**  
Авторизация выполняется при помощи JWT токена.  
Страница регистрации: http://localhost:8080/api-auth/signup/  
Страница получения JWT токена: http://localhost:8080/api-auth/login/  

Для авторизации в заголовке запроса необходимо указать:  
```
Authorization: Bearer <token>
```
