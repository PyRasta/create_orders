# Тестовое задание
Программа рассчитана на фьючерсы


## Содержание
- [Настройка](#настройка)
- [Запуск](#запуск)


## Настройка
Заносим ключи в окружение:
```bash
export API_KEY=your_api_key
export API_SECRET=your_api_secret
```


## Запуск
Для работы программы нужен python3.10+.
Сборка
```bash
$ git clone https://github.com/PyRasta/test_task_.git <your project name>
$ cd <your project name>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn main:app --reload     
```
Запуск
```bash
$ uvicorn main:app --reload   
```
Переходим на локальный адрес в браузере, http://127.0.0.1:8000

## Вся промежуточная информация выводится в консоли