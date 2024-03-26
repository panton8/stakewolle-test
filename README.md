# Проект развернут по адресу:
* http://3.81.48.187:8000/
# Документация: 
*  http://3.81.48.187:8000/swagger/ 
*  http://3.81.48.187:8000/redoc/
# Ссылка на Postman коллекцию: 
* https://api.postman.com/collections/27103406-aca4697e-29a9-4ad4-8975-86dc5f675fdc?access_key=PMAT-01HSRCZE8NJG0TZ5XTJPSJG01X

# Endpoints:
## api/auth/register/

### Пример тела запроса:
##### {
#####    "username": "stakewolle",
#####    "first_name": "Stake",
#####    "last_name": "Wolle",
#####    "password": "12345678",
#####    "email": "stakewolle@yopmail.com"
##### }
## (при регистрации с помощью реферального кода необходимо указать доп. параметр: "referral_code":	"68Z1Y2ML" (на данный момент единственный действующий реферальный код в системе), после этого хозяин кода получает 20 бонусных баллов, а новый пользователь — 8)

### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/65f3f53d-cf89-4aa6-b071-03a318f0fe78)
--------------------------------------------

## api/auth/login/
### Пример тела запроса:
##### {
#####    "email": "stakewolle@yopmail.com"
#####    "password": "12345678",
##### } 

### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/95a4e450-d15e-4ef2-bc1d-a2bea8535be1)
--------------------------------------------

## api/auth/refresh/
### Пример тела запроса:
##### {
#####        "refresh" : "A.B.C"
##### }

### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/dfaa4424-7714-4b6b-a301-b826c2a2760e)
 --------------------------------------------

## api/user/
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/7eff8e85-caea-483f-8392-9af2bf259d8d)
--------------------------------------------

## api/user/{id}/
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/f8a94099-49b3-4121-ac79-f9990fb8a1bf)
--------------------------------------------

## api/referral_code/ (генерация/ренегерация кода или получение кода для запрашиваемого пользователя)
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/5c62d73b-b034-4ece-b6ab-cec4fb90bb7b)
--------------------------------------------

## api/referrals/ (все рефералы запрашиваемого пользователя)
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/77e4a6c8-0e1e-4979-9c79-36e9f60648e2)
--------------------------------------------

## api/referrals/{id}/ (все рефералы пользователя с указанным ID)
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/4b0c2c4c-ee43-44f8-83db-aa54e6a7e59a)
--------------------------------------------

## api/share/ 
### Пример тела запроса:
##### {
#####    "email": "stakewolle@yopmail.com"
##### } 

### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/9191ff3e-512d-46d2-86d1-87e2bf0ab01f)
--------------------------------------------

## api/code/delete_code/ 
### Ожидаемый результат:
![image](https://github.com/panton8/stakewolle-test/assets/91150058/c25e331e-219b-4bbf-91c7-d97646736853) или ![image](https://github.com/panton8/stakewolle-test/assets/91150058/6e212195-70fd-4a65-a2cf-c06bd6a12484)
